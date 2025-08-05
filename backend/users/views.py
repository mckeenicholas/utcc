from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from .models import Person
from .serializers import PersonSerializer

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
    queryset = Person.objects.all().order_by('name')
    serializer_class = PersonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=["get"])
    def search(self, request):
        """
        Custom action to search persons by name.
        Usage: GET /persons/search/?name=searchterm
        """
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
