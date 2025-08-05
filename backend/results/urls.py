from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CompetitionViewSet,
    ResultViewSet,
    CompetitionResultsAPIView,
    RecordsListAPIView,
)

# Create router for ViewSets
router = DefaultRouter()
router.register(r"competitions", CompetitionViewSet, basename="competition")
router.register(r"results", ResultViewSet, basename="result")

urlpatterns = [
    # Custom API endpoints
    path("records/", RecordsListAPIView.as_view(), name="records-list"),
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
