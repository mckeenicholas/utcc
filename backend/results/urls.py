from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CompetitionSessionViewSet,
    CompetitionViewSet,
    ResultViewSet,
    CompetitionResultsAPIView,
    RecordsListAPIView,
    RankingsAPIView,
    SessionCompetitionsAPIView,
)

# Create router for ViewSets
router = DefaultRouter()
router.register(r"competitions", CompetitionViewSet, basename="competition")
router.register(r"results", ResultViewSet, basename="result")
router.register(r"session", CompetitionSessionViewSet, basename="session")

urlpatterns = [
    # Custom API endpoints
    path("records/", RecordsListAPIView.as_view(), name="records-list"),
    path("rankings/", RankingsAPIView.as_view(), name="rankings"),
    path(
        "session/<int:session_id>/competitions/",
        SessionCompetitionsAPIView.as_view(),
        name="session-competitions-list",
    ),
    path(
        "competitions/latest/results/",
        CompetitionResultsAPIView.as_view(),
        name="latest-competition-results",
    ),
    path(
        "competitions/<int:competition_id>/results/",
        CompetitionResultsAPIView.as_view(),
        name="competition-results-detail",
    ),
    # Include router URLs for CRUD operations
    # This provides:
    # - GET/POST /competitions/
    # - GET/PUT/PATCH/DELETE /competitions/{id}/
    # - POST/GET/PUT/PATCH/DELETE /results/{id}/ (GET /results/ disabled)
    path("", include(router.urls)),
]
