from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from unittest.mock import patch
from products.models import Products
from dashboard.views import AuthorizedDashboardView, SummaryPageView


class AuthorizedDashboardViewTest(TestCase):
    def setUp(self):
        # Set up a test client
        self.client = Client()

        # Create a test user
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_authorized_dashboard_view_requires_login(self):
        """
        Test that the AuthorizedDashboardView requires login.
        """
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)  # Should redirect to login

        # Log in the user
        self.client.login(username="testuser", password="testpassword")

        # Now, access the view after login
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)  # Should be successful

    def test_authorized_dashboard_context_data(self):
        """
        Test the context data returned by AuthorizedDashboardView.
        """
        # Log in the user
        self.client.login(username="testuser", password="testpassword")

        # Make a GET request to the AuthorizedDashboardView
        response = self.client.get(reverse("dashboard"))

        # Check that the response status code is 200 (successful)
        self.assertEqual(response.status_code, 200)

        # Check the context data
        self.assertIn("products", response.context)
        self.assertIn("products_count", response.context)


class SummaryPageViewTest(TestCase):
    def setUp(self):
        # Set up a test client
        self.client = Client()

        # Create a test user
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_summary_page_view_requires_login(self):
        """
        Test that the SummaryPageView requires login.
        """
        response = self.client.get(reverse("summary"))
        self.assertEqual(response.status_code, 302)  # Should redirect to login

        # Log in the user
        self.client.login(username="testuser", password="testpassword")

        # Now, access the view after login
        response = self.client.get(reverse("summary"))
        self.assertEqual(response.status_code, 200)  # Should be successful

    def test_summary_page_context_data(self):
        """
        Test the context data returned by SummaryPageView.
        """
        # Log in the user
        self.client.login(username="testuser", password="testpassword")

        # Make a GET request to the SummaryPageView
        response = self.client.get(reverse("summary"))

        # Check that the response status code is 200 (successful)
        self.assertEqual(response.status_code, 200)

        # Check the context data
        self.assertIn("products_count", response.context)
