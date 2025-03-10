from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Competition, Result
from itertools import groupby
from operator import attrgetter


def results_list(_, competition_id=None):
    if competition_id:
        competition = get_object_or_404(Competition, pk=competition_id)
    else:
        competition = Competition.objects.latest("date")

    results = Result.objects.filter(competition=competition).order_by("event", "round")

    # Group results by event
    events_data = {}
    for event, event_results in groupby(results, key=attrgetter("event")):
        event_results = list(event_results)
        rounds_data = {}

        # Group by round within each event
        for round_num, round_results in groupby(event_results, key=attrgetter("round")):
            round_results = list(round_results)
            persons_data = []

            for result in round_results:
                person_data = {
                    "name": result.name,
                    "times": result.get_all_times_display(),
                }
                persons_data.append(person_data)

            rounds_data[round_num] = persons_data

        events_data[event] = {
            "name": dict(Result.EVENT_CHOICES)[event],
            "rounds": rounds_data,
        }

    return JsonResponse(
        {
            "competition": {
                "name": competition.name,
                "date": competition.date.isoformat(),
            },
            "results": events_data,
        }
    )


def competition_list(request):
    competitions = Competition.objects.all().order_by("-date")
    competitions_data = [
        {"id": comp.id, "name": comp.name, "date": comp.date.isoformat()}
        for comp in competitions
    ]

    return JsonResponse({"competitions": competitions_data})
