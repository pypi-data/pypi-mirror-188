from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse


class TenantPermissionRequiredMixin(PermissionRequiredMixin):
    """Verify for SingleObjectViews that the user has required permissions, and
    the object's tenant matches the user's tenant.
    """

    def has_permission(self):
        user = self.request.user
        obj = self.get_object()
        return user.tenant == obj.tenant and user.has_perms(
            self.get_permission_required()
        )


class AnonymousRequiredMixin(PermissionRequiredMixin):
    """View mixin that only allows access for anonymous users."""

    def has_permission(self):
        # TODO: instead of a 403, redirect to LOGIN_REDIRECT_URL

        if not self.request.user.is_anonymous:
            redirect(reverse(settings.LOGIN_REDIRECT_URL))
        return True
