from django.contrib import admin
from django.urls import path, include
from auth_app.views import VisiterRedirectionView

urlpatterns = [
    # Admin site URL pattern
    path("admin/", admin.site.urls),
    # Include authentication app URLs
    path("auth/", include("auth_app.urls")),
    # Include dashboard app URLs
    path("dashboard/", include("dashboard.urls")),
    # Include products app URLs
    path("products/", include("products.urls")),
    # Default URL pattern, redirecting visitors to a specific view
    path("", VisiterRedirectionView.as_view(), name="visiter_redirect"),
]
