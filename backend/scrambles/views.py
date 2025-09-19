# Scramble API View
# This file contains the API view for handling scramble sets.

from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Max
from .models import Scramble, ScrambleSet, Competition
from .serializers import ScrambleSerializer, ScrambleSetSerializer


class RoundScrambles(APIView):
    """
    API view to handle scramble sets for a specific competition, event, and round.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, competition_id, event_id, round_id, format=None):
        """
        Accepts a list of scramble objects and saves them as a new scramble set.
        The scramble_set number is auto-incremented, but the scramble_num is taken
        directly from the POST data.
        """
        # Validate that the request data is a list of dictionaries
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

        # Get the competition object
        try:
            competition = Competition.objects.get(pk=competition_id)
        except Competition.DoesNotExist:
            return Response(
                {"detail": "Competition not found."}, status=status.HTTP_404_NOT_FOUND
            )

        # Determine the next scramble_set number for this competition/event/round
        last_set = (
            ScrambleSet.objects.filter(
                competition=competition, event=event_id, round=round_id
            ).aggregate(max_set=Max("scramble_set"))["max_set"]
            or 0
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

        # Iterate through the submitted scramble objects and create new model instances
        for scramble_obj in scramble_objects:
            s = Scramble(
                scramble_set=scr_set,
                scramble_num=scramble_obj["scramble_num"],
                scramble=scramble_obj["scramble"],
            )

            s.save()

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
