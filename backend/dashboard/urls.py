from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path(
        "competition/<int:competition_id>/",
        views.competition_detail,
        name="competition_detail",
    ),
    path(
        "competition/delete/<int:competition_id>/",
        views.delete_competition_view,
        name="delete_competition",
    ),
    path(
        "competition/<int:competition_id>/result/<int:result_id>/edit/",
        views.edit_result_view,
        name="edit_result",
    ),
    path(
        "competition/<int:competition_id>/result/<int:result_id>/delete/",
        views.delete_result_view,
        name="delete_result",
    ),
]
