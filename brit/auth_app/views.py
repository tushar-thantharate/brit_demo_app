from django.contrib.auth.models import User
from django.http.response import HttpResponse as HttpResponse
from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import RedirectView

from auth_app.forms import UserAuthenticationForm, SignUpFormView


class LoginFormView(FormView):
    """
    View for handling user authentication (login).
    """

    template_name = "login.html"
    form_class = UserAuthenticationForm

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Redirects authenticated users to the dashboard
        if self.request.user.is_authenticated:
            redirect_to = self.get_success_url()
            return redirect(redirect_to)

        response = super().dispatch(request, *args, **kwargs)
        # XSS-Protection
        response["X-Frame-Options"] = "sameorigin"
        return response

    def get_success_url(self):
        # Defines the URL to redirect to upon successful login
        return "dashboard"

    def form_valid(self, form):
        # Logs in the user and redirects to the success URL
        auth_login(self.request, form.get_user())
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class LogoutView(View):
    """
    View for handling user logout.
    """

    def get(self, request):
        # Logs out the user and redirects to the login page
        if request.user.is_authenticated:
            auth_logout(self.request)
        return redirect("login")


class SignUpFormView(FormView):
    """
    View for handling user registration (signup).
    """

    template_name = "signup.html"
    form_class = SignUpFormView

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            redirect_to = self.get_success_url()
            return redirect(redirect_to)

        response = super().dispatch(request, *args, **kwargs)
        response["X-Frame-Options"] = "sameorigin"
        return response

    def get_success_url(self):
        return "dashboard"

    def form_valid(self, form):
        # Creates a new user upon successful form submission
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        first_name = form.cleaned_data.get("first_name")
        last_name = form.cleaned_data.get("last_name")
        if username and password:
            user = User.objects.get_or_create(username=username)[0]
            user.email = username
            user.first_name = first_name
            user.last_name = last_name
            user.set_password(password)
            user.save()

        return redirect(self.get_success_url())

    def form_invalid(self, form):
        # Renders the signup form with errors if invalid form submission
        return self.render_to_response(self.get_context_data(form=form))


class VisiterRedirectionView(RedirectView):
    """
    View for redirecting visitors based on their authentication status.
    """

    def get(self, request, *args, **kwargs):
        # If the user is anonymous, redirect to the login page
        if self.request.user.is_anonymous:
            return redirect("login")

        # If the user is authenticated, redirect to the dashboard
        return redirect("dashboard")
