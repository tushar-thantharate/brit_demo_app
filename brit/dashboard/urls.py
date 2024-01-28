from django.urls import path, re_path

from .views import AuthorizedDashboardView, SummaryPageView

urlpatterns = [
    # URL pattern for the authorized dashboard view
    path("details", AuthorizedDashboardView.as_view(), name="dashboard"),
    # URL pattern for the summary page view
    path("summary", SummaryPageView.as_view(), name="summary"),
]
