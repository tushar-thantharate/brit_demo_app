from django.urls import path

from .views import LoginFormView, LogoutView, SignUpFormView

urlpatterns = [
    # URL pattern for the login view
    path("login", LoginFormView.as_view(), name="login"),
    # URL pattern for the logout view
    path("logout", LogoutView.as_view(), name="logout"),
    # URL pattern for the signup view
    path("signup", SignUpFormView.as_view(), name="signup"),
]
