from itertools import groupby
from collections import defaultdict

from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action

from results.models import Result
from .models import Person
from .serializers import PersonSerializer


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Username and password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            session_id = request.session.session_key
            return Response(
                {"message": "Login successful", "sessionid": session_id},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)


@ensure_csrf_cookie
def get_csrf(request):
    return JsonResponse({"message": "CSRF cookie set"})


def is_logged_in(request):
    logged_in = request.user.is_authenticated
    return JsonResponse({"logged_in": logged_in})


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all().order_by("name")
    serializer_class = PersonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=["get"])
    def search(self, request):
        name_query = request.query_params.get("name", "").strip()

        if not name_query:
            return Response(
                {"error": "Please provide a 'name' parameter to search"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        persons = Person.objects.filter(name__icontains=name_query).order_by("name")[
            :20
        ]
        serializer = self.get_serializer(persons, many=True)

        return Response(serializer.data)


class PersonResultsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, person_id, format=None):
        person = get_object_or_404(Person, id=person_id)

        results_qs = (
            Result.objects.filter(person=person.id)
            .select_related("competition", "competition__session")
            .order_by("event", "-competition__date", "round")
        )

        results_list = list(results_qs)

        if not results_list:
            return Response(
                {
                    "person": {"id": person.id, "name": person.name},
                    "records": {},
                    "results": [],
                },
                status=status.HTTP_200_OK,
            )

        best_times = self._calculate_best_times(results_list)

        event_list = self._group_results_by_event(results_list)

        return Response(
            {
                "person": {"id": person.id, "name": person.name},
                "records": best_times,
                "results": event_list,
            }
        )

    def _calculate_best_times(self, results_list):
        best_times = defaultdict(
            lambda: {"single": float("inf"), "average": float("inf")}
        )

        for result in results_list:
            event = result.event

            if result.single > 0:
                best_times[event]["single"] = min(
                    best_times[event]["single"], result.single
                )

            if result.average > 0:
                best_times[event]["average"] = min(
                    best_times[event]["average"], result.average
                )

        cleaned_best_times = {}
        for event, times in best_times.items():
            cleaned_best_times[event] = {
                "single": times["single"] if times["single"] != float("inf") else None,
                "average": times["average"]
                if times["average"] != float("inf")
                else None,
            }

        return cleaned_best_times

    def _group_results_by_event(self, results_list):
        event_list = []

        for event_name, event_results in groupby(results_list, key=lambda r: r.event):
            competition_groups = []
            event_results_list = list(event_results)

            for competition, comp_results in groupby(
                event_results_list, key=lambda r: r.competition
            ):
                rounds = []
                comp_results_list = list(comp_results)

                for result in comp_results_list:
                    rounds.append(
                        {
                            "round": result.round,
                            "times": result.get_times(),
                            "single": result.single,
                            "average": result.average,
                        }
                    )

                competition_groups.append(
                    {
                        "id": competition.id,
                        "name": competition.name,
                        "date": competition.date,
                        "rounds": rounds,
                    }
                )

            event_list.append(
                {
                    "event": event_name,
                    "competitions": competition_groups,
                }
            )

        return event_list
