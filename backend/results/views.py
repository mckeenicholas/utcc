from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import THREE_ATTEMPT_EVENTS, Competition, Result
from itertools import groupby
from operator import attrgetter


def results_list(_, competition_id=None):
    if competition_id:
        competition = get_object_or_404(Competition, pk=competition_id)
    else:
        try:
            competition = Competition.objects.latest("date")
        except Competition.DoesNotExist:
            return JsonResponse(
                {"message": "No competitions exist"}, status=404
            )  # Added status

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
                all_times = result.get_times()
                if result.event in THREE_ATTEMPT_EVENTS:
                    displayed_times = all_times[:3]
                else:
                    displayed_times = all_times

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
