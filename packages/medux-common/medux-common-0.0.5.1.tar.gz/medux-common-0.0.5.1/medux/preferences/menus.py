from django.urls import reverse_lazy

from medux.common.api.interfaces import IMenuItem
from django.utils.translation import gettext_lazy as _


class Preferences(IMenuItem):
    menu = "user"
    title = _("Preferences")
    url = reverse_lazy("preferences:index")
    icon = "gear"
