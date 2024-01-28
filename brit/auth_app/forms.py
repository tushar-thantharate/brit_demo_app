import unicodedata
from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError
from django.utils.text import capfirst

UserModel = get_user_model()


class UsernameField(forms.CharField):
    def to_python(self, value):
        # Normalize Unicode characters for consistent handling
        return unicodedata.normalize("NFKC", super().to_python(value))

    def widget_attrs(self, widget):
        # Set widget attributes for consistent behavior (e.g., no autocapitalization)
        return {
            **super().widget_attrs(widget),
            "autocapitalize": "none",
            "autocomplete": "username",
        }


class UserAuthenticationForm(forms.Form):
    username = UsernameField(
        label="Email",
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
                "class": "form-control",
                "placeholder": "Email",
                "required": "required",
            }
        ),
    )
    password = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "class": "form-control",
                "placeholder": "Password",
                "required": "required",
            }
        ),
    )

    error_messages = {
        "invalid_login": "Please enter a correct %(username)s and password. Note that both "
        "fields may be case-sensitive.",
        "inactive": "This account is inactive.",
        "invalid_otp": "Wrong OTP",
    }

    def __init__(self, request=None, *args, **kwargs):
        # The 'request' parameter is set for custom auth use by subclasses.
        # The form data comes in via the standard 'data' kwarg.
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        # Set username field properties dynamically based on the user model
        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        username_max_length = self.username_field.max_length or 254
        self.fields["username"].max_length = username_max_length
        self.fields["username"].widget.attrs["maxlength"] = username_max_length
        if self.fields["username"].label is None:
            self.fields["username"].label = capfirst(self.username_field.verbose_name)

    def clean(self):
        # Validate the username and password, authenticate the user
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data

    def confirm_login_allowed(self, user):
        # Confirm if the user is allowed to log in (e.g., check if the account is active)
        if not user.is_active:
            raise ValidationError(
                self.error_messages["inactive"],
                code="inactive",
            )

    def get_user(self):
        # Get the authenticated user
        return self.user_cache

    def get_invalid_login_error(self):
        # Raise an error for invalid login attempts
        self.add_error("username", self.error_messages["invalid_login"])
        return ValidationError(
            self.error_messages["invalid_login"], code="invalid_login"
        )


class SignUpFormView(forms.Form):
    username = UsernameField(
        label="Email",
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
                "class": "form-control",
                "placeholder": "Email",
                "required": "required",
            }
        ),
    )
    password = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "class": "form-control",
                "placeholder": "Password",
                "required": "required",
            }
        ),
    )
    first_name = forms.CharField(
        label="First_name",
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
                "class": "form-control",
                "placeholder": "First Name",
                "required": "required",
            }
        ),
    )
    last_name = forms.CharField(
        label="Last_Name",
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
                "class": "form-control",
                "placeholder": "Last Name",
                "required": "required",
            }
        ),
    )

    error_messages = {
        "invalid_login": "Please enter a correct %(username)s and password. Note that both "
        "fields may be case-sensitive.",
        "inactive": "This account is inactive.",
    }

    def __init__(self, request=None, *args, **kwargs):
        # Initialize the SignUpFormView
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        # Set username field properties dynamically based on the user model
        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        username_max_length = self.username_field.max_length or 254
        self.fields["username"].max_length = username_max_length
        self.fields["username"].widget.attrs["maxlength"] = username_max_length
        if self.fields["username"].label is None:
            self.fields["username"].label = capfirst(self.username_field.verbose_name)
