from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout,
    Row,
    Column,
    ButtonHolder,
    Submit,
    LayoutObject,
    HTML,
)
from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import (
    UserCreationForm as DjangoUserCreationForm,
    UsernameField,
)
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from medux.common.bootstrap import Card
from medux.common.constants import USERS_GROUP_NAME
from medux.core.models import User
from medux.common.models import Tenant
from .mixins import ErrorLogMixin


class SignUpForm(DjangoUserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": _("Username"), "class": "form-control"}
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"placeholder": _("Email"), "class": "form-control"}
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": _("Password"),
                "class": "form-control",
                "autocomplete": "new-password",
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": _("Password check"),
                "class": "form-control",
                "autocomplete": "new-password",
            }
        )
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class UserCreationForm(ErrorLogMixin, DjangoUserCreationForm):
    class Meta:
        model = User
        localized_fields = "__all__"
        fields = [
            "tenant",
            "username",
            "title",
            "first_name",
            "last_name",
            "email",
            "is_active",
            "is_superuser",
            "is_staff",
            "groups",
        ]
        field_classes = {"username": UsernameField}

    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(**kwargs)
        self.fields["tenant"].initial = self.user.tenant
        self.fields["is_staff"].initial = True
        self.fields["groups"].initial = [Group.objects.get(name="Users")]
        # self.fields["date_joined"].widget = forms.HiddenInput()

        # self.fields["date_joined"].disabled = True

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Card(
                Row(Column("username"), Column("tenant")),
                Row(
                    Column("title", css_class="col-2"),
                    Column("first_name"),
                    Column("last_name"),
                ),
                Row(Column("email")),
                Row(Column("password1")),
                Row(Column("password2")),
                Row(
                    Column("groups"),
                    Column("is_active"),
                    Column("is_staff"),
                    Column("is_superuser"),
                ),
                # title=_("Username: {username}").format(username=self.user.username),
                # subtitle=_("Created at: {date_joined}").format(
                #     date_joined=strftime(
                #         self.user.date_joined.date(), settings.SHORT_DATE_FORMAT
                #     )
                # ),
            ),
            ButtonHolder(
                Submit("submit", _("Save")),
                Submit("delete", _("Delete"), css_class="btn-danger"),
            ),
        )

        # self.helper.add_input(Button("cancel", _("Cancel"), css_class="btn-secondary"))

    def clean_groups(self):
        if not self.cleaned_data["groups"]:
            return [Group.objects.get(name=USERS_GROUP_NAME)]
        return self.cleaned_data["groups"]


# class AddLayout(Layout):
#     """Crispy Layout with enabled += operator"""
#
#     # FIXME: https://github.com/django-crispy-forms/django-crispy-forms/issues/1307
#     def __iadd__(self, other) -> None:
#         self.fields.append(other)
#
#     def __add__(self, other: LayoutObject) -> "AddLayout":
#         new = copy(self)
#         new += other
#         return new


class UserProfileSectionFormMixin:
    """Mixin for all User profile sections.

    It provides a ``helper`` attribute, which is a crispy FormHelper()
    instance to your usage - don't declare another form helper.
    The helper's layout is auto-generated from the models fields as provided.
    If a ``layout`` attr is given, this layout is taken.
    If a ``buttons`` attr is given, these buttons are appended to the form.
    As default, a "Save" button is defined.

    The form requires the current `request` as kwarg.
    """

    #: the crispy layout of the form. If empty, the usual form fields are taken.
    layout: Layout = None

    #: The buttons at the bottom of the form. A "Save" button as default.
    buttons: list[LayoutObject] = [Submit("submit", _("Save"))]

    def __init__(self, request, *args, **kwargs) -> None:
        self.request = request
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = self.get_layout()
        super().__init__(*args, **kwargs)

    def get_layout(self) -> Layout:
        """return the declared layout, or if none, build a standard Layout
        of the original field names of the form class."""
        if not self.layout:
            self.layout = Layout(*[field for field in self.base_fields])

        return Layout(*self.layout.fields + [ButtonHolder(*self.buttons)])


class UserProfileMasterDataForm(UserProfileSectionFormMixin, ModelForm):
    class Meta:
        model = User
        localized_fields = "__all__"
        fields = [
            # "username",
            "tenant",
            "title",
            "first_name",
            "last_name",
            "email",
            "avatar",
        ]

    layout = Layout(
        Row(
            Column("title", css_class="col-2"),
            Column("first_name"),
            Column("last_name"),
        ),
        Row(Column("email"), Column("tenant")),
        Row(
            Column("avatar"),
            Column(
                HTML(
                    """{% load static %}
                    <span class='avatar avatar-xl mb-3'
                    style='background-image: url({% if object.avatar %}{{object.avatar.url}}{% else %}
                    {% static "images/default_avatar.png" %}{% endif %})'>
                    """
                ),
            ),
        ),
        # subtitle=_("Created at: {date_joined}").format(
        #     date_joined=strftime(
        #         self.user.date_joined.date(), settings.SHORT_DATE_FORMAT
        #     )
        # ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.request.user.is_superuser:
            self.fields["tenant"].queryset = Tenant.objects.filter(
                id=self.instance.tenant.id
            )
            self.fields["tenant"].disabled = True


class UserProfilePasswordForm(UserProfileSectionFormMixin, forms.ModelForm):
    """
    A form that lets a user change set their password without entering the old
    password.
    """

    class Meta:
        model = User
        fields = ["id"]

    # FIXME - better inherit SetPasswordForm directly - but it must be fixed first: uses "user" instead of
    #  "instance" as parameter...
    # This view is copied from django.contrib.auth.forms.SetPasswordForm,
    # as this form needs a "user" argument instead of "instance", this
    # makes it incompatible with other UserProfileSectionForms
    error_messages = {
        "password_mismatch": _("The two password fields didn’t match."),
    }
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    self.error_messages["password_mismatch"],
                    code="password_mismatch",
                )
        password_validation.validate_password(password2, self.instance)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.instance.set_password(password)
        if commit:
            self.instance.save()
        return self.instance


class UserProfileGroupsForm(UserProfileSectionFormMixin, ModelForm):
    class Meta:
        model = User
        fields = ["groups", "is_active"]

    layout = Layout(Row(Column("groups"), Column("is_active")))

    groups = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(), queryset=Group.objects.all()
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["is_active"].disabled = not self.request.user.is_superuser
        if not self.request.user.is_superuser:
            self.fields["is_active"].widget = forms.HiddenInput()
