
from django.urls import path

from .views import (
    UploadCSVView,
    ReconciliationView,
    ReconciliationResultsView,
    DashboardSummaryView
)

urlpatterns = [

    path(
        "upload/<str:system>/",
        UploadCSVView.as_view(),
        name="upload-csv"
    ),

    path(
        "reconcile/",
        ReconciliationView.as_view(),
        name="reconcile"
    ),

    path(
        "results/",
        ReconciliationResultsView.as_view(),
        name="reconciliation-results"
    ),

    path(
        "dashboard/",
        DashboardSummaryView.as_view(),
        name="dashboard-summary"
    ),

]
