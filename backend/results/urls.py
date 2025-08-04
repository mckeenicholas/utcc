from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CompetitionViewSet,
    ResultViewSet,
    CompetitionResultsAPIView,
    RecordsListAPIView,
)

router = DefaultRouter()
router.register(r"competitions", CompetitionViewSet, basename="competition")
router.register(r"results", ResultViewSet, basename="result")

urlpatterns = [
    path(
        "results/latest/",
        CompetitionResultsAPIView.as_view(),
        name="latest-results-list",
    ),
    # /competitions/ (GET, POST)
    # /competitions/<id>/ (GET, PUT, PATCH, DELETE)
    # /results/ (GET, POST)
    # /results/<id>/ (GET, PUT, PATCH, DELETE)
    path("", include(router.urls)),
    path(
        "competitions/<int:competition_id>/results",
        CompetitionResultsAPIView.as_view(),
        name="competition-results-list",
    ),
    path("records/", RecordsListAPIView.as_view(), name="records-list"),
]
