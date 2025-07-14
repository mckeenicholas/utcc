from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Competition, Result
from itertools import groupby
from operator import attrgetter
from django.db.models import F, Window
from django.db.models.functions import RowNumber


def results_list(_, competition_id=None):
    if competition_id:
        competition = get_object_or_404(Competition, pk=competition_id)
    else:
        try:
            competition = Competition.objects.latest("date")
        except Competition.DoesNotExist:
            return JsonResponse({"message": "No competitions exist"}, status=404)

    results = Result.objects.filter(competition=competition).order_by("event", "round")

    # Group results by event
    events_data = []
    for event_code, event_results_iterable in groupby(results, key=attrgetter("event")):
        event_results = list(event_results_iterable)
        rounds_data = []

        for round_num, round_results_iterable in groupby(
            event_results, key=attrgetter("round")
        ):
            round_results = list(round_results_iterable)
            persons_data = []

            for result in round_results:
                displayed_times = result.get_times()

                person_data = {
                    "name": result.name,
                    "times": displayed_times,
                    "single": result.single,
                    "average": result.average,
                }
                persons_data.append(person_data)

            rounds_data.append({"round": round_num, "results": persons_data})

        events_data.append({"event": event_code, "rounds": rounds_data})

    return JsonResponse(
        {
            "competition": {
                "name": competition.name,
                "date": competition.date.isoformat(),
            },
            "results": events_data,
        }
    )


def competition_list(_):
    competitions = Competition.objects.all().order_by("-date")
    competitions_data = [
        {"id": comp.id, "name": comp.name, "date": comp.date.isoformat()}
        for comp in competitions
    ]

    return JsonResponse({"competitions": competitions_data})


def records_list(_):
    records = {}

    # Annotate each result with a row number partitioned by event, ordered by single and average
    best_singles = (
        Result.objects.filter(single__gt=0)
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
        Result.objects.filter(average__gt=0)
        .annotate(
            row_num=Window(
                expression=RowNumber(),
                partition_by=[F("event")],
                order_by=F("average").asc(),
            )
        )
        .filter(row_num=1)
    )

    # Build the records dictionary from the optimized queries
    for result in best_averages:
        if result.event not in records:
            records[result.event] = {}

        records[result.event]["average"] = {
            "result": result.average,
            "times_list": result.get_times(),
            "person": result.name,
            "competition_name": result.competition.name,
            "competition_id": result.competition.id,
        }

    # Having an average always implies a single, however
    # the order of results isn't guaranteed to be the same.
    for result in best_singles:
        if result.event not in records:
            records[result.event] = {}

        records[result.event]["single"] = {
            "result": result.single,
            "times_list": result.get_times(),
            "person": result.name,
            "competition_name": result.competition.name,
            "competition_id": result.competition.id,
        }

    return JsonResponse(records)
