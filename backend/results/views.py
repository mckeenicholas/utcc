from collections import defaultdict
from itertools import groupby
from operator import attrgetter

from django.db.models import F, Window
from django.db.models.functions import RowNumber
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Competition, Result
from .serializers import (
    CompetitionSerializer,
    FullCompetitionResultsSerializer,
    RecordDetailSerializer,
    ResultCreateUpdateSerializer,
)


class CompetitionViewSet(viewsets.ModelViewSet):
    queryset = Competition.objects.all().order_by("-date")
    serializer_class = CompetitionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # Use the default settings for pagination (PageNumberPagination with page_size=20)


class ResultViewSet(viewsets.ModelViewSet):
    queryset = (
        Result.objects.select_related("person_id").all().order_by("event", "round")
    )
    serializer_class = ResultCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Listing all results is disabled as there can be a lot of them, and it doesn't really make sense with how the data is stored.
    def list(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Check if a result already exists for this person, event, round, and competition
        person_id = serializer.validated_data.get("person_id")
        event = serializer.validated_data.get("event")
        round_num = serializer.validated_data.get("round")
        competition = serializer.validated_data.get("competition")

        existing_result = Result.objects.filter(
            person_id=person_id, event=event, round=round_num, competition=competition
        ).first()

        if existing_result:
            # Update the existing result
            for attr, value in serializer.validated_data.items():
                setattr(existing_result, attr, value)
            existing_result.save()

            # Return the updated result
            response_serializer = self.get_serializer(existing_result)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        else:
            # Create new result as normal
            return super().create(request, *args, **kwargs)


class CompetitionResultsAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, competition_id=None, format=None):
        if competition_id:
            competition = get_object_or_404(Competition, pk=competition_id)
        else:
            competition = Competition.objects.order_by("-date").first()
            if not competition:
                return Response(
                    {"message": "No competitions exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )

        results = (
            Result.objects.filter(competition=competition)
            .select_related("person_id")
            .order_by("event", "round")
        )

        events_data = []
        for event_code, event_results_iter in groupby(results, key=attrgetter("event")):
            event_results = list(event_results_iter)
            rounds_data = []

            for round_num, round_results_iter in groupby(
                event_results, key=attrgetter("round")
            ):
                round_results = list(round_results_iter)
                rounds_data.append({"round": round_num, "results": round_results})

            events_data.append({"event": event_code, "rounds": rounds_data})

        final_data = {"competition": competition, "results": events_data}
        serializer = FullCompetitionResultsSerializer(final_data)
        return Response(serializer.data)


class RecordsListAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        records = defaultdict(dict)

        best_singles = (
            Result.objects.select_related("person_id", "competition")
            .filter(single__gt=0)
            .annotate(
                row_num=Window(
                    expression=RowNumber(),
                    partition_by=[F("event")],
                    order_by=F("single").asc(),
                )
            )
            .filter(row_num=1)
        )

        best_averages = (
            Result.objects.select_related("person_id", "competition")
            .filter(average__gt=0)
            .annotate(
                row_num=Window(
                    expression=RowNumber(),
                    partition_by=[F("event")],
                    order_by=F("average").asc(),
                )
            )
            .filter(row_num=1)
        )

        for result in best_averages:
            serializer = RecordDetailSerializer(
                result, context={"record_type": "average"}
            )
            records[result.event]["average"] = serializer.data

        for result in best_singles:
            serializer = RecordDetailSerializer(
                result, context={"record_type": "single"}
            )
            records[result.event]["single"] = serializer.data

        return Response(records)
