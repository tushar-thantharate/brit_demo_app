from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from auth_app.views import LoginFormView


class VisiterRedirectionViewTest(TestCase):
    def test_anonymous_user_redirects_to_login(self):
        """
        Test that an anonymous user is redirected to the login page.
        """
        # Create an instance of the VisiterRedirectionView
        response = self.client.get(reverse("visiter_redirect"))

        # Check that the response is a redirect
        self.assertEqual(response.status_code, 302)

        # Check that the redirect goes to the login page
        self.assertRedirects(response, reverse("login"))

    def test_authenticated_user_redirects_to_dashboard(self):
        """
        Test that an authenticated user is redirected to the dashboard.
        """
        # Create a test user
        test_user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

        # Log in the user
        self.client.login(username="testuser", password="testpassword")

        # Create an instance of the VisiterRedirectionView
        response = self.client.get(reverse("visiter_redirect"))

        # Check that the response is a redirect
        self.assertEqual(response.status_code, 302)

        # Check that the redirect goes to the dashboard
        self.assertRedirects(response, reverse("dashboard"))


class LogoutViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.test_user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

        # Log in the user for testing
        self.client = Client()
        self.client.login(username="testuser", password="testpassword")

    def test_authenticated_user_logs_out_and_redirects_to_login(self):
        """
        Test that an authenticated user logs out and is redirected to the login page.
        """
        # Ensure the user is initially logged in
        self.assertEqual(int(self.client.session["_auth_user_id"]), self.test_user.pk)

        # Make a GET request to the LogoutView
        response = self.client.get(reverse("logout"))

        # Check that the response is a redirect
        self.assertEqual(response.status_code, 302)

        # Check that the redirect goes to the login page
        self.assertRedirects(response, reverse("login"))

        # Ensure the user is now logged out
        self.assertFalse(self.client.session.keys(), "_auth_user_id")


class SignUpFormViewTest(TestCase):
    def setUp(self):
        # Set up a test client
        self.client = Client()

    def test_authenticated_user_redirected_to_dashboard(self):
        """
        Test that an authenticated user is redirected to the dashboard.
        """
        # Create a test user
        user = User.objects.create_user(username="testuser", password="testpassword")

        # Log in the user
        self.client.login(username="testuser", password="testpassword")

        # Make a GET request to the SignUpFormView
        response = self.client.get(reverse("signup"))

        # Check that the response is a redirect
        self.assertEqual(response.status_code, 302)

        # Check that the redirect goes to the dashboard
        self.assertRedirects(response, reverse("dashboard"))

    def test_valid_form_submission_creates_user_and_redirects_to_dashboard(self):
        """
        Test that a valid form submission creates a new user and redirects to the dashboard.
        """
        # Make a POST request to the SignUpFormView with valid form data
        response = self.client.post(
            reverse("signup"),
            {
                "username": "newuser",
                "password": "newpassword",
                "first_name": "John",
                "last_name": "Doe",
            },
        )

        # Check that the response is a redirect
        self.assertEqual(response.status_code, 302)

        # Check that the redirect goes to the dashboard
        self.assertEqual(response.url, reverse("dashboard"))

        # Check that the new user is created in the database
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_invalid_form_submission_renders_signup_form_with_errors(self):
        """
        Test that an invalid form submission renders the signup form with errors.
        """
        # Make a POST request to the SignUpFormView with invalid form data
        response = self.client.post(reverse("signup"), {"username": "invaliduser"})

        # Check that the response status code is 200 (form submission unsuccessful)
        self.assertEqual(response.status_code, 200)

        # Check that the user is not created in the database
        self.assertFalse(User.objects.filter(username="invaliduser").exists())


class LoginFormViewTest(TestCase):
    def setUp(self):
        # Set up a test client
        self.client = Client()

        # Create a test user for authentication
        self.test_user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_authenticated_user_redirected_to_dashboard(self):
        """
        Test that an authenticated user is redirected to the dashboard.
        """
        # Log in the user
        self.client.login(username="testuser", password="testpassword")

        # Make a GET request to the LoginFormView
        response = self.client.get(reverse("login"))

        # Check that the response is a redirect
        self.assertEqual(response.status_code, 302)

        # Check that the redirect goes to the dashboard
        self.assertRedirects(response, reverse("dashboard"))

    def test_get_success_url(self):
        """
        Test that the get_success_url method returns the correct URL.
        """
        view = LoginFormView()
        success_url = view.get_success_url()

        # Check that the success URL is "dashboard"
        self.assertEqual(success_url, "dashboard")

    def test_valid_form_submission_logs_in_user_and_redirects_to_dashboard(self):
        """
        Test that a valid form submission logs in the user and redirects to the dashboard.
        """
        # Make a POST request to the LoginFormView with valid form data
        response = self.client.post(
            reverse("login"),
            {
                "username": "testuser",
                "password": "testpassword",
            },
        )

        # Check that the response is a redirect
        self.assertEqual(response.status_code, 302)

        # Check that the redirect goes to the dashboard
        self.assertRedirects(response, reverse("dashboard"))

    def test_invalid_form_submission_renders_login_form_with_errors(self):
        """
        Test that an invalid form submission renders the login form with errors.
        """
        # Make a POST request to the LoginFormView with invalid form data
        response = self.client.post(reverse("login"), {"username": "invaliduser"})

        # Check that the response status code is 200 (form submission unsuccessful)
        self.assertEqual(response.status_code, 200)

        # Check that the user is not logged in
        self.assertFalse(User.objects.filter(username="invaliduser").exists())

    def test_xss_protection_header_present(self):
        """
        Test that the X-Frame-Options header is present in the response for XSS protection.
        """
        # Make a GET request to the LoginFormView
        response = self.client.get(reverse("login"))

        # Check that the X-Frame-Options header is present
        self.assertIn("X-Frame-Options", response)

    def test_dispatch_redirects_authenticated_user_to_dashboard(self):
        """
        Test that the dispatch method redirects authenticated users to the dashboard.
        """
        # Log in the user
        self.client.login(username="testuser", password="testpassword")

        # Make a GET request to the LoginFormView
        response = self.client.get(reverse("login"))

        # Check that the response is a redirect
        self.assertEqual(response.status_code, 302)

        # Check that the redirect goes to the dashboard
        self.assertRedirects(response, reverse("dashboard"))
