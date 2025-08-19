from collections import defaultdict
from itertools import groupby
from operator import attrgetter

from django.db.models import F, Window
from django.db.models.functions import RowNumber
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from django.conf import settings

from .models import Competition, CompetitionSession, Result
from .serializers import (
    CompetitionSerializer,
    CompetitionSessionSerializer,
    FullCompetitionResultsSerializer,
    RecordDetailSerializer,
    ResultCreateUpdateSerializer,
)


class CompetitionSessionViewSet(viewsets.ModelViewSet):
    queryset = CompetitionSession.objects.all().order_by("-start_date")
    serializer_class = CompetitionSessionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = None


class CompetitionViewSet(viewsets.ModelViewSet):
    queryset = Competition.objects.all().order_by("-date")
    serializer_class = CompetitionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # Use the default settings for pagination (PageNumberPagination with page_size=20)

    def get_queryset(self):
        queryset = self.queryset
        session_id = self.request.query_params.get("session_id")

        if session_id is not None:
            queryset = queryset.filter(session__id=session_id)

        return queryset


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
        session_id = request.query_params.get("session_id")

        if competition_id:
            competition = get_object_or_404(Competition, pk=competition_id)
        else:
            competition_query = Competition.objects.order_by("-date")
            if session_id:
                competition_query = competition_query.filter(session_id=session_id)
            competition = competition_query.first()

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
        session_id = request.query_params.get("session_id")

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

        if session_id:
            best_singles = best_singles.filter(competition__session_id=session_id)
            best_averages = best_averages.filter(competition__session_id=session_id)

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


class RankingsAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        session_id = request.query_params.get("session_id")

        # Get query parameters
        event = request.query_params.get("event")
        result_format = request.query_params.get("type")  # 'single' or 'average'
        all_results = request.query_params.get("all", "false").lower() == "true"
        page = int(request.query_params.get("page", 1))

        # Validate required parameters
        if not event:
            return Response(
                {"error": "Event parameter is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not result_format or result_format not in ["single", "average"]:
            return Response(
                {"error": "Format parameter must be 'single' or 'average'"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Build base queryset
        queryset = Result.objects.select_related("person_id", "competition").filter(
            event=event
        )

        # Filter by session if provided
        if session_id:
            queryset = queryset.filter(competition__session_id=session_id)

        # Filter by format and exclude zero/invalid times
        if result_format == "single":
            queryset = queryset.filter(single__gt=0).order_by("single")
        else:  # average
            queryset = queryset.filter(average__gt=0).order_by("average")

        # If not showing all results, get only best result per person
        if not all_results:
            if result_format == "single":
                queryset = queryset.annotate(
                    row_num=Window(
                        expression=RowNumber(),
                        partition_by=[F("person_id")],
                        order_by=F("single").asc(),
                    )
                ).filter(row_num=1)
            else:  # average
                queryset = queryset.annotate(
                    row_num=Window(
                        expression=RowNumber(),
                        partition_by=[F("person_id")],
                        order_by=F("average").asc(),
                    )
                ).filter(row_num=1)

        # Paginate results
        paginator = Paginator(queryset, settings.PAGE_SIZE)
        page_obj = paginator.get_page(page)

        # Build next and previous URLs
        request_url = request.build_absolute_uri()
        base_url = request_url.split("?")[0]  # Remove existing query params

        next_url = None
        if page_obj.has_next():
            next_params = request.GET.copy()
            next_params["page"] = page_obj.next_page_number()
            next_url = f"{base_url}?{next_params.urlencode()}"

        previous_url = None
        if page_obj.has_previous():
            prev_params = request.GET.copy()
            prev_params["page"] = page_obj.previous_page_number()
            previous_url = f"{base_url}?{prev_params.urlencode()}"

        # Serialize results
        serialized_results = []
        for rank, result in enumerate(
            page_obj.object_list, start=(page - 1) * settings.PAGE_SIZE + 1
        ):
            serializer = RecordDetailSerializer(
                result, context={"record_type": result_format}
            )
            result_data = serializer.data
            result_data["rank"] = rank
            serialized_results.append(result_data)

        return Response(
            {
                "count": paginator.count,
                "next": next_url,
                "previous": previous_url,
                "results": serialized_results,
            }
        )
