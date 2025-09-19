from django.urls import path
from .views import RoundScrambleSet, RoundScrambles, ScrambleVisibility

urlpatterns = [
    path(
        "<int:competition_id>/<slug:event_id>/<int:round_id>/",
        RoundScrambles.as_view(),
        name="round-scramble",
    ),
    path(
        "<int:competition_id>/<int:set_id>/",
        RoundScrambleSet.as_view(),
        name="round-scramble-set",
    ),
    path(
        "<int:competition_id>/<int:set_id>/visibility/",
        ScrambleVisibility.as_view(),
        name="round-scramble-visibility",
    ),
]
