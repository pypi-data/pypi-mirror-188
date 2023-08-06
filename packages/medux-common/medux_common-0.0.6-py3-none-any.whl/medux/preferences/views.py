from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import TemplateView


class PreferencesView(PermissionRequiredMixin, TemplateView):
    template_name = "preferences/preferences.html"

    def has_permission(self):
        return self.request.user.is_employee
