from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.bootstrap import InlineField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit
from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm as DjangoAuthenticationForm,
    UserCreationForm as DjangoUserCreationForm,
)
from django.utils.translation import gettext as _

from medux.common.api.interfaces import ILoginFormExtension
from medux.common.bootstrap import Card
from medux.core.models import User


class AuthenticationForm(DjangoAuthenticationForm):
    """Extendable MedUX login form"""

    # TODO: use this in MedUX Online, but not in MedUX
    # remember_me = forms.BooleanField(
    #     label=_("Remember me"), widget=forms.CheckboxInput(), required=False
    # )

    class Meta:
        model = User
        fields = (
            "username",
            "password",
            *[e.field_names for e in ILoginFormExtension],
        )

    @property
    def media(self):
        """Merge all extensions' media."""
        media = super().media
        for extension in ILoginFormExtension:
            if hasattr(extension, "Media"):
                js = extension.Media.js if hasattr(extension.Media, "js") else ()
                css = extension.Media.css if hasattr(extension.Media, "css") else {}
                media += forms.Media(js=js, css=css)
        return media

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].help_text = ""
        self.fields["username"].widget.attrs.update({"autofocus": True})
        self.fields["password"].help_text = ""
        for extension in ILoginFormExtension:
            extension.alter_fields(self.fields)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Card(
                FloatingField("username"),
                FloatingField("password"),
                # InlineField("remember_me"),
                title=_("Login"),
            ),
            ButtonHolder(Submit("submit", _("Log in"), css_class="w-100 btn-lg")),
        )
        for extension in ILoginFormExtension:
            extension.alter_layout(self.helper.layout)

    def clean(self):
        cleaned_data = super().clean()
        for extension in ILoginFormExtension:
            cleaned_data = extension.clean(self.cleaned_data)
        return cleaned_data


class SignUpForm(DjangoUserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Username", "class": "form-control"}
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Email", "class": "form-control"})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password", "class": "form-control"}
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password check", "class": "form-control"}
        )
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
