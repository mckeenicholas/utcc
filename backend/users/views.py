from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.db.models import Min
from .models import Person
from .serializers import PersonSerializer
from results.models import Result
from itertools import groupby
from django.shortcuts import get_object_or_404

# Create your views here.


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
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
        name_query = request.query_params.get("name", None)
        if name_query:
            persons = Person.objects.filter(name__icontains=name_query)
            serializer = self.get_serializer(persons, many=True)
            return Response(serializer.data)
        else:
            return Response(
                {"error": "Please provide a 'name' parameter to search"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class PersonResultsAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, person_id, format=None):
        person = get_object_or_404(Person, id=person_id)

        records_qs = (
            Result.objects.filter(person_id=person.id, average__gt=0)
            .values("event")
            .annotate(best_single=Min("single"), best_average=Min("average"))
        )

        best_times = {
            r["event"]: {"single": r["best_single"], "average": r["best_average"]}
            for r in records_qs
        }

        results_qs = (
            Result.objects.filter(person_id=person.id)
            .select_related("competition")
            .order_by("event", "-competition__date", "round")
        )

        event_list = []
        for event_name, event_results in groupby(results_qs, key=lambda r: r.event):
            competition_groups = []
            for competition, comp_results in groupby(
                event_results, key=lambda r: r.competition
            ):
                rounds = [
                    {
                        "round": r.round,
                        "times": r.get_times(),
                        "single": r.single,
                        "average": r.average,
                    }
                    for r in comp_results
                ]
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

        return Response(
            {
                "person": {"id": person.id, "name": person.name},
                "records": best_times,
                "results": event_list,
            }
        )
