from django.urls import path

from .views import (
    RoundScrambleSet,
    ScrambleGenerator,
    ScrambleVisibility,
)

urlpatterns = [
    path(
        "<int:competition_id>/<slug:event_id>/<int:round_id>/generate/",
        ScrambleGenerator.as_view(),
        name="request-generate-scrambles",
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
