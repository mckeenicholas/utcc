from django.urls import path
from .views import LoginView, LogoutView, get_csrf, is_logged_in

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("csrf/", get_csrf, name="get_csrf"),
    path("loginstatus/", is_logged_in, name="check_login"),
]
