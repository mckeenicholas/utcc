# Scramble API View
# This file contains the API view for handling scramble sets.

from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Max
from .models import Scramble, ScrambleSet, Competition
from .serializers import ScrambleSerializer, ScrambleSetSerializer
from django.db import transaction


class RoundScrambles(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, competition_id, event_id, round_id, format=None):
        scramble_objects = request.data
        if not isinstance(scramble_objects, list) or not all(
            isinstance(s, dict) and "scramble" in s and "scramble_num" in s
            for s in scramble_objects
        ):
            return Response(
                {
                    "detail": "Expected a list of scramble objects with 'scramble' and 'scramble_num' keys."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if len(scramble_objects) > 7:
            return Response(
                {"detail": "At most 7 scrambles can be submitted at once."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            with transaction.atomic():
                competition = Competition.objects.get(pk=competition_id)

                scramble_sets = ScrambleSet.objects.select_for_update().filter(
                    competition=competition, event=event_id, round=round_id
                )

                last_set = (
                    scramble_sets.aggregate(max_set=Max("scramble_set"))["max_set"] or 0
                )
                next_set = last_set + 1

                scr_set = ScrambleSet(
                    competition=competition,
                    event=event_id,
                    round=round_id,
                    scramble_set=next_set,
                    visible=False,
                )
                scr_set.save()

                scrambles_to_create = [
                    Scramble(
                        scramble_set=scr_set,
                        scramble_num=scramble_obj["scramble_num"],
                        scramble=scramble_obj["scramble"],
                    )
                    for scramble_obj in scramble_objects
                ]

                Scramble.objects.bulk_create(scrambles_to_create)

        except Competition.DoesNotExist:
            return Response(
                {"detail": "Competition not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ScrambleSetSerializer(scr_set)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RoundScrambleSet(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, set_id, competition_id):
        scrambles = Scramble.objects.filter(
            scramble_set=set_id, scramble_set__competition=competition_id
        ).order_by("scramble_num")

        serializer = ScrambleSerializer(scrambles, many=True)

        if not scrambles.exists():
            return Response(
                {"detail": "No scrambles found"}, status=status.HTTP_404_NOT_FOUND
            )

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
        delete_records = ScrambleSet.objects.filter(
            pk=set_id, competition=competition_id
        )

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
