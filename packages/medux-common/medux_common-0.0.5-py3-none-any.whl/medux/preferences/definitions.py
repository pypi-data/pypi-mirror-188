from django.db import models
from django.utils.translation import gettext_lazy as _


class Scope(models.IntegerChoices):
    VENDOR = 1, _("Vendor")
    TENANT = 2, _("Tenant")
    GROUP = 3, _("Group")
    DEVICE = 4, _("Device")
    USER = 5, _("User")


class ScopeIcons(models.TextChoices):
    VENDOR = "box2"  # -fill
    TENANT = "person-badge"  # -fill
    GROUP = "people"  # -fill
    DEVICE = "display"  # -fill
    USER = "person"  # -fill


class KeyType(models.TextChoices):
    BOOLEAN = "bool"
    STRING = "str"  # short string
    INTEGER = "int"
    TEXT = "text"  # long text
