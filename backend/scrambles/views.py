# Scramble API View
# This file contains the API view for handling scramble sets.
import requests
from django.db import transaction
from django.db.models import Max
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from results.models import Result

from .models import Competition, Scramble, ScrambleSet
from .serializers import ScrambleSerializer, ScrambleSetSerializer

SCRAMBLE_SERVICE_ENDPOINT = "http://utcc-scramble-generator:8080"
SCRAMBLE_NUMS = [-2, -1, 1, 2, 3, 4, 5]


class RoundScrambleSet(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, set_id, competition_id):
        scrambles = Scramble.objects.filter(
            scramble_set=set_id,
            scramble_set__competition=competition_id,
        ).order_by("scramble_num")

        serializer = ScrambleSerializer(scrambles, many=True)

        if not scrambles.exists():
            return Response({"detail": "No scrambles found"}, status=status.HTTP_404_NOT_FOUND)

        scramble_set = scrambles.first().scramble_set
        competition = scramble_set.competition

        response_data = {
            "competition": competition.name,
            "event": scramble_set.event,
            "round": scramble_set.round,
            "scrambles": serializer.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)

    def delete(self, request, competition_id, set_id):
        delete_records = ScrambleSet.objects.filter(pk=set_id, competition=competition_id)

        num_deleted = len(delete_records)
        delete_records.delete()

        return Response({"deleted": num_deleted}, status=status.HTTP_200_OK)


class ScrambleVisibility(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, set_id, competition_id):
        visibility = request.data.get("visibility")

        if visibility is None or not isinstance(visibility, bool):
            return Response(
                {"error": "Field 'visibility' must be provided and must be a boolean."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        records = ScrambleSet.objects.filter(pk=set_id, competition=competition_id)

        num_updated = len(records)
        records.update(visible=visibility)

        return Response({"updated": num_updated}, status=status.HTTP_200_OK)


class ScrambleGenerator(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, competition_id, event_id, round_id):
        if event_id not in Result.Event.values:
            return Response(
                {"error": "event_id is not a valid WCA event."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        count = request.data.get("count")
        if not count or not isinstance(count, int) or not (0 < count <= 7):
            return Response(
                {"error": "count must be an integer in (0, 7]"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        sets = request.data.get("numSets")
        if not sets or not isinstance(sets, int) or sets <= 0:
            return Response(
                {"error": "numSets must be a positive integer."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        competition = get_object_or_404(Competition, pk=competition_id)

        try:
            response = requests.post(
                f"{SCRAMBLE_SERVICE_ENDPOINT}/api/scrambles",
                json={"puzzleType": event_id, "count": sets * count},
                headers={"Content-Type": "application/json"},
                timeout=30,
            )

            response.raise_for_status()
            scrambles = response.json()

        except requests.exceptions.RequestException as e:
            return Response(
                {"error": f"Failed to generate scrambles: {e}"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        try:
            with transaction.atomic():
                scramble_sets_qs = ScrambleSet.objects.select_for_update().filter(
                    competition=competition,
                    event=event_id,
                    round=round_id,
                )
                last_set = scramble_sets_qs.aggregate(max_set=Max("scramble_set"))["max_set"] or 0
                next_set_number = last_set + 1

                scramble_sets_to_create = []
                for set_idx in range(sets):
                    scr_set = ScrambleSet(
                        competition=competition,
                        event=event_id,
                        round=round_id,
                        scramble_set=next_set_number + set_idx,
                        visible=False,
                    )
                    scramble_sets_to_create.append(scr_set)

                ScrambleSet.objects.bulk_create(scramble_sets_to_create)

                scrambles_to_create = []
                scramble_counter = 0
                for scr_set in scramble_sets_to_create:
                    for scramble_num in SCRAMBLE_NUMS[:count]:
                        scrambles_to_create.append(
                            Scramble(
                                scramble_set=scr_set,
                                scramble_num=scramble_num,
                                scramble=scrambles[scramble_counter],
                            ),
                        )
                        scramble_counter += 1

                Scramble.objects.bulk_create(scrambles_to_create)

        except Competition.DoesNotExist:
            return Response({"detail": "Competition not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ScrambleSetSerializer(scramble_sets_to_create, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
