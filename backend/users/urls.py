from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoginView, LogoutView, get_csrf, is_logged_in, PersonViewSet

# Create router for CRUD operations
router = DefaultRouter()
router.register(r"persons", PersonViewSet, basename="person")

urlpatterns = [
    # Authentication endpoints
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("auth/csrf/", get_csrf, name="get_csrf"),
    path("auth/status/", is_logged_in, name="check_login"),
    # Include router URLs for CRUD operations
    # This provides:
    # - POST/GET/PUT/PATCH/DELETE /persons/{id}/ (GET /persons/ disabled)
    # - TOOD: GET /persons/search/?name=searchterm
    path("", include(router.urls)),
]
