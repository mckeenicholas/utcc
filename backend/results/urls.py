from django.urls import path
from . import views

app_name = "results"

urlpatterns = [
    path("", views.results_list, name="results_list"),
    path(
        "<int:competition_id>/", views.results_list, name="results_list_by_competition"
    ),
    path("competitions/", views.competition_list, name="competition_list"),
]
