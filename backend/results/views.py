from collections import defaultdict
from itertools import groupby
from operator import attrgetter

from django.conf import settings
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import F, OuterRef, Subquery, Window
from django.db.models.functions import Rank, RowNumber
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from scrambles.models import ScrambleSet

from .models import Competition, CompetitionSession, Result
from .serializers import (
    CompetitionSerializer,
    CompetitionSessionSerializer,
    FullCompetitionResultsSerializer,
    RankingSerializer,
    RecordDetailSerializer,
    ResultCreateUpdateSerializer,
)


class CompetitionSessionViewSet(viewsets.ModelViewSet):
    queryset = CompetitionSession.objects.all().order_by("-start_date")
    serializer_class = CompetitionSessionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = None


class SessionCompetitionsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, session_id, format=None):
        get_object_or_404(CompetitionSession, pk=session_id)

        competitions = (
            Competition.objects.prefetch_related("results")
            .filter(session=session_id)
            .order_by("-date")
        )
        serializer = CompetitionSerializer(competitions, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CompetitionViewSet(viewsets.ModelViewSet):
    serializer_class = CompetitionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = (
            Competition.objects.select_related("session")
            .prefetch_related("results")
            .order_by("-date")
        )
        session_id = self.request.query_params.get("session_id")

        if session_id is not None:
            queryset = queryset.filter(session__id=session_id)

        return queryset


class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.select_related("person").all().order_by("event", "round")
    serializer_class = ResultCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Listing all results is disabled as there can be a lot of them, and it doesn't really make sense with how the data is stored.
    def list(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        unique_fields = {
            "person": validated_data.get("person"),
            "event": validated_data.get("event"),
            "round": validated_data.get("round"),
            "competition": validated_data.get("competition"),
        }

        defaults = {k: v for k, v in validated_data.items() if k not in unique_fields}

        try:
            instance, created = Result.objects.update_or_create(**unique_fields, defaults=defaults)
        except IntegrityError as e:
            print(e)

            return Response(
                {"detail": "Error creating or updating result."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        response_serializer = self.get_serializer(instance)
        return Response(response_serializer.data, status=status_code)


class CompetitionResultsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, competition_id=None, format=None):
        session_id = request.query_params.get("session_id")
        uoft_status = request.query_params.get("uoft")

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
            .select_related("person")
            .order_by("event", "round")
        )

        if uoft_status == "1":
            results = results.filter(person__is_uoft_student=True)
        elif uoft_status == "0":
            results = results.filter(person__is_uoft_student=False)

        scramble_sets = (
            ScrambleSet.objects.filter(competition=competition, visible=True)
            .prefetch_related("scrambles")
            .order_by("event", "round", "scramble_set")
        )

        scramble_sets_by_event_round = {}
        for scramble_set in scramble_sets:
            key = (scramble_set.event, scramble_set.round)

            if key not in scramble_sets_by_event_round:
                scramble_sets_by_event_round[key] = []
            scramble_sets_by_event_round[key].append(scramble_set)

        events_data = []
        for event_code, event_results_iter in groupby(results, key=attrgetter("event")):
            event_results = list(event_results_iter)
            rounds_data = []

            for round_num, round_results_iter in groupby(event_results, key=attrgetter("round")):
                round_results = list(round_results_iter)

                round_scramble_sets = scramble_sets_by_event_round.get((event_code, round_num), [])

                rounds_data.append(
                    {
                        "round": round_num,
                        "results": round_results,
                        "scramble_sets": round_scramble_sets,
                    },
                )

            events_data.append({"event": event_code, "rounds": rounds_data})

        final_data = {"competition": competition, "results": events_data}
        serializer = FullCompetitionResultsSerializer(final_data)
        return Response(serializer.data)


class RecordsListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        session_id = request.query_params.get("session_id")
        uoft_status = request.query_params.get("uoft")

        records = defaultdict(dict)

        best_singles = (
            Result.objects.select_related("person", "competition")
            .filter(single__gt=0)
            .annotate(
                row_num=Window(
                    expression=RowNumber(),
                    partition_by=[F("event")],
                    order_by=F("single").asc(),
                ),
            )
            .filter(row_num=1)
        )

        best_averages = (
            Result.objects.select_related("person", "competition")
            .filter(average__gt=0)
            .annotate(
                row_num=Window(
                    expression=RowNumber(),
                    partition_by=[F("event")],
                    order_by=F("average").asc(),
                ),
            )
            .filter(row_num=1)
        )

        if session_id:
            best_singles = best_singles.filter(competition__session_id=session_id)
            best_averages = best_averages.filter(competition__session_id=session_id)

        if uoft_status == "1":
            best_singles = best_singles.filter(person__is_uoft_student=True)
            best_averages = best_averages.filter(person__is_uoft_student=True)
        elif uoft_status == "0":
            best_singles = best_singles.filter(person__is_uoft_student=False)
            best_averages = best_averages.filter(person__is_uoft_student=False)

        for result in best_averages:
            serializer = RecordDetailSerializer(result, context={"record_type": "average"})
            records[result.event]["average"] = serializer.data

        for result in best_singles:
            serializer = RecordDetailSerializer(result, context={"record_type": "single"})
            records[result.event]["single"] = serializer.data

        return Response(records)


class RankingsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        session_id = request.query_params.get("session_id")
        uoft_status = request.query_params.get("uoft")

        event = request.query_params.get("event")
        result_format = request.query_params.get("type")  # 'single' or 'average'
        all_results = request.query_params.get("all", "false").lower() == "true"
        page = int(request.query_params.get("page", 1))

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

        queryset = Result.objects.select_related("person", "competition").filter(event=event)

        if session_id:
            queryset = queryset.filter(competition__session_id=session_id)

        if uoft_status == "1":
            queryset = queryset.filter(person__is_uoft_student=True)
        elif uoft_status == "0":
            queryset = queryset.filter(person__is_uoft_student=False)

        field = "single" if result_format == "single" else "average"

        if result_format == "single":
            queryset = queryset.filter(single__gt=0)
        else:
            queryset = queryset.filter(average__gt=0)

        if not all_results:
            best_results_subquery = (
                Result.objects.filter(person=OuterRef("person"), event=event, **{f"{field}__gt": 0})
                .order_by(field)
                .values("id")[:1]
            )
            queryset = queryset.filter(id__in=Subquery(best_results_subquery))

        queryset = queryset.annotate(
            rank=Window(expression=Rank(), order_by=F(field).asc()),
        ).order_by(field, "rank")

        paginator = Paginator(queryset, settings.PAGE_SIZE)
        page_obj = paginator.get_page(page)

        request_url = request.build_absolute_uri()
        base_url = request_url.split("?")[0]

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

        serialized_results = []
        for result in page_obj.object_list:
            serializer = RankingSerializer(result, context={"record_type": result_format})
            result_data = serializer.data
            serialized_results.append(result_data)

        return Response(
            {
                "count": paginator.count,
                "next": next_url,
                "previous": previous_url,
                "results": serialized_results,
            },
        )


class CompetitionScramblesAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, competition_id):
        scramble_sets = (
            ScrambleSet.objects.filter(competition_id=competition_id)
            .values("id", "event", "round", "scramble_set", "visible")
            .order_by("event", "round", "scramble_set")
        )

        # Group by event -> round -> list of set objects
        grouped_data = defaultdict(lambda: defaultdict(list))

        for s_set in scramble_sets:
            event = s_set["event"]
            round_num = s_set["round"]
            grouped_data[event][round_num].append(
                {
                    "id": s_set["id"],
                    "scramble_set": s_set["scramble_set"],
                    "visible": s_set["visible"],
                },
            )

        result = []
        for event, rounds in sorted(grouped_data.items()):
            rounds_list = [
                {"round": round_num, "sets": sets} for round_num, sets in sorted(rounds.items())
            ]
            result.append({"event": event, "rounds": rounds_list})

        return Response(result)
