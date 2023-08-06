from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView

from .multiple import MultipleFormsView, MultipleFormsMixin
from ..api.interfaces import IUserProfileSection, UseComponentMixin, ILoginViewExtension
from ..auth.forms import AuthenticationForm
from ..mixins import AnonymousRequiredMixin
from ..models import Tenant

__all__ = [MultipleFormsView, MultipleFormsMixin]

User = get_user_model()


class LoginView(AnonymousRequiredMixin, DjangoLoginView):
    """Extendable login view with welcome message"""

    form_class = AuthenticationForm
    template_name = "common/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for plugin in ILoginViewExtension:
            context.update(plugin.alter_context_data(**kwargs))

        context["welcome_message"] = _("Medically welcome to {project_title}").format(
            project_title=settings.PROJECT_TITLE
        )

        return context

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        for plugin in ILoginViewExtension:
            plugin.alter_response(request, response, *args, **kwargs)
        return response

    def form_valid(self, form):
        response = super().form_valid(form)
        for plugin in ILoginViewExtension:
            plugin.form_valid(form, response)
        return response


class FormActionsMixin:
    """Mixin to add to UpdateViews that enables additional action buttons.

    Each action is mapped to the corresponding method in the view, so a
    button named "delete" calls the ``delete()`` method.
    Actions available:
    * delete
    """

    # TODO: add wildcard buttons - is this a security risk?
    def post(self, request, *args, **kwargs):
        if request.POST.get("delete", ""):
            return self.delete(request, *args, **kwargs)
        else:
            return super().post(request, *args, **kwargs)


class DashboardMixin:
    """Add common needed dashboard attributes to the context.

    All views that live in the dashboard must inherit from this mixin.
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"tenants": Tenant.objects.all().order_by("last_name")})
        return context


class UserUpdateView(
    PermissionRequiredMixin, DashboardMixin, UseComponentMixin, DetailView
):
    """The view for user data updates.

    This view doesn't have to be a UpdateView. It does not update data itself.
    The actual forms processing and user data updating is done in plugins.
    """

    model = User
    permission_required = "core.change_user"
    template_name = "common/user_change_form.html"
    components = [IUserProfileSection]


class UserProfileView(UserUpdateView):
    """A user update view, with the current authenticated user as model."""

    def has_permission(self):
        return self.request.user.is_authenticated

    def get_object(self, queryset=None):
        return self.request.user


class AutoFocusMixin:
    """Put the 'autofocus' attribute to a given field of a FormView.

    Set the autofocus attribute to a field of the form you are working
    with, and it will get the focus after loading the page.
    """

    # FIXME: move AutoFocusMixin to medux.common

    autofocus_field_name = None

    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        form = super().get_form(form_class)

        if self.autofocus_field_name in form.fields:
            form.fields[self.autofocus_field_name].widget.attrs.update(
                {"autofocus": True}
            )
        return form
