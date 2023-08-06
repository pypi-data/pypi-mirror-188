import calendar
import random

from django.contrib import messages
from django.db.models import IntegerChoices, TextChoices
from django.utils.translation import gettext_lazy as _

LEVEL_ICONS = {
    messages.DEBUG: "bug-fill",
    messages.INFO: "info-circle-fill",
    messages.SUCCESS: "check2-circle",
    messages.WARNING: "exclamation-triangle-fill",
    messages.ERROR: "exclamation-square-fill",
}

USERS_GROUP_NAME = "Users"


class DaysOfWeek(IntegerChoices):
    SUNDAY = (calendar.SUNDAY, _("Sunday"))
    MONDAY = (calendar.MONDAY, _("Monday"))
    TUESDAY = (calendar.TUESDAY, _("Tuesday"))
    WEDNESDAY = (calendar.WEDNESDAY, _("Wednesday"))
    THURSDAY = (calendar.THURSDAY, _("Thurstay"))
    FRIDAY = (calendar.FRIDAY, _("Friday"))
    SATURDAY = (calendar.SATURDAY, _("Saturday"))


class TimeSpans(TextChoices):
    YEARLY = "Y", _("yearly")
    MONTHLY = "M", _("monthly")
    WEEKLY = "W", _("weekly")
    DAILY = "D", _("daily")


class UserColors(TextChoices):
    DARK = "dark"
    # WHITE = "white"
    AZURE = "azure"
    INDIGO = "indigo"
    PURPLE = "purple"
    PINK = "pink"
    RED = "red"
    ORANGE = "orange"
    YELLOW = "yellow"
    LIME = "lime"


def random_user_color():
    """Returns a random UserColors value"""
    return random.choice(UserColors.choices)[0]
