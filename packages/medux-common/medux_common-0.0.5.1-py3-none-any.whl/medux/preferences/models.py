#  MedUX - Open Source Electronical Medical Record
#  Copyright (c) 2022  Christian González
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.conf import settings
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from medux.common.models import Tenant
from medux.preferences.definitions import Scope, KeyType, ScopeIcons
from medux.preferences.registry import PreferencesRegistry


def validate_lower(value):
    if not value == value.lower():
        raise ValidationError("%(value)s must be lowercase.", params={"value": value})


class BasePreference(models.Model):
    """Basic model which holds namespace and key of a setting.
    ScopedPreference use this model as FK, to prevent redundant storage of preferences."""

    class Meta:
        verbose_name = verbose_name_plural = _("Settings")
        ordering = ["namespace", "key"]

    namespace = models.CharField(max_length=25, validators=[validate_lower])
    key = models.CharField(max_length=255, validators=[validate_lower])

    def clean(self):
        """Make sure namespace and key are lowercase."""
        self.namespace = str(self.namespace).lower()
        self.key = str(self.key).lower()

    @classmethod
    def namespaces(cls) -> list[str]:
        """:return: a list of available namespaces."""
        # FIXME this is highly insufficient. distinct() would be better, but not available on SQLite/dev
        result = set()
        for s in cls.objects.order_by("namespace").values_list("namespace", flat=True):
            result.add(s)
        return list(result)

    @classmethod
    def keys(cls) -> list[tuple[str, str]]:
        """:return: a tuple[namespace,key] of all currently available keys."""

        return list(set((item.namespace, item.key) for item in cls.objects.all()))

    @property
    def icon(self):
        """:return: the preferences' icon name."""
        return PreferencesRegistry.icon(self.namespace, self.key)

    @property
    def key_type(self) -> KeyType:
        """:return: the setting's key type.

        This is a convenience method and gets it from the PreferencesRegistry."""
        return PreferencesRegistry.key_type(self.namespace, self.key)

    @property
    def help_text(self) -> str:
        """:return: the setting's help_text.
        This is a convenience method and gets it from the PreferencesRegistry."""
        return PreferencesRegistry.help_text(self.namespace, self.key)

    def __str__(self):
        return f"{self.namespace}.{self.key}"


class ScopedPreference(models.Model):
    """Model class for all scoped MedUX preferences.

    Preferences are generally saved as strings, but are interpreted at retrieval
    and cast into their correct types. ScopedPreference knows about
    ``str``, ``int``, ``bool``

    You can easily access preferences using CachedPreferences.get(namespace, key, scope, ...)
    """

    class Meta:
        verbose_name = verbose_name_plural = _("Scoped preferences")
        ordering = ["base__namespace", "base__key", "scope"]
        unique_together = [
            ["base", "scope", "tenant"],
            ["base", "scope", "group"],
            # TODO: ["base", "scope", "device"],
            ["base", "scope", "user"],
        ]
        permissions = [
            (
                "change_own_user_scopedpreference",
                _("Can change own user's preferences"),
            ),
            (
                "change_own_tenant_scopedpreference",
                _("Can change own tenant's preferences"),
            ),
            (
                "change_own_group_scopedpreference",
                _("Can change own groups' preferences"),
            ),
            ("change_device_scopedpreference", _("Can change a device's preferences")),
        ]

    base = models.ForeignKey(
        BasePreference, on_delete=models.CASCADE, related_name="scopedpreferences"
    )
    """The FK to the basic preferences fields like namespace, key."""

    tenant = models.ForeignKey(
        Tenant,
        verbose_name=_("Tenant"),
        on_delete=models.CASCADE,
        default=None,
        null=True,
        blank=True,
    )
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, default=None, null=True, blank=True
    )
    # device = models.ForeignKey(
    #     "Device", on_delete=models.CASCADE, default=None, null=True, blank=True
    # )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default=None,
        null=True,
        blank=True,
    )

    scope = models.IntegerField(choices=Scope.choices)
    """The scope where this setting is valid."""

    value = models.CharField(max_length=255, null=True)
    """The value of the setting. NULL means the setting using this scope
    was deleted, and the next matching scope is used."""

    @property
    def namespace(self):
        """:return: The preferences' namespace"""
        return self.base.namespace

    @property
    def key(self):
        """:return: The preferences' key"""
        return self.base.key

    @property
    def icon(self):
        """:return: the preferences' icon name."""
        return self.base.icon

    @property
    def key_type(self) -> KeyType:
        """:return: the preferences's key type.

        This is a convenience method and gets it from the PreferencesRegistry."""
        return self.base.key_type

    @property
    def help_text(self) -> str:
        return self.base.help_text

    def clean(self):
        """Check if object FK is present if scope demands it."""

        # Make value a str
        if self.value is None:
            self.value = ""
        self.value = self.value.strip()
        # Scopes with their correct object FK
        if self.scope == Scope.USER:
            if not self.user:
                raise ValidationError(_("If scope is 'user', a user must be provided"))
        elif self.scope == Scope.DEVICE:
            if not self.device:
                raise ValidationError(
                    _("If scope is 'device', a device must be provided")
                )
        elif self.scope == Scope.GROUP:
            if not self.group:
                raise ValidationError(
                    _("If scope is 'group', a group must be provided")
                )
        elif self.scope == Scope.TENANT:
            if not self.tenant:
                raise ValidationError(
                    _("If scope is 'tenant', a tenant must be provided")
                )
        # TODO check if user/device/group is filled in if scope is one of them

    @classmethod
    def keys(cls) -> list[tuple[str, str]]:
        """:return: a Tuple[namespace,key] of all currently available keys."""

        return BasePreference.keys()

    @classmethod
    def namespaces(cls) -> list[str]:
        """:return: a list of available namespaces."""
        return BasePreference.namespaces()

    def __str__(self) -> str:
        # add user, tenant, group
        fk = ""
        if self.scope == Scope.USER:
            fk = f": '{self.user}'"
        elif self.scope == Scope.GROUP:
            fk = f": '{self.group}'"
        elif self.scope == Scope.TENANT:
            fk = f": '{self.tenant}'"
        a = f"{'.'.join([self.base.namespace, self.base.key])} [{Scope(self.scope).name}{fk}]: {self.value}"
        return a

    @classmethod
    def assure_exists(cls, namespace, key, scope) -> None:
        """Raises KeyError if given preferences are not registered."""
        if not PreferencesRegistry.exists(namespace, key, scope):
            raise KeyError(f"Setting {namespace}.{key}/{scope.name} is not registered.")

    def get_scope_icon(self) -> str:
        """:return: the icon name of the preferences' scope."""
        if not self.scope:
            return ""
        scope = Scope(self.scope)
        return ScopeIcons[scope.name].value if scope else ""

    def get_related_object(self):
        match self.scope:
            case Scope.TENANT:
                return self.tenant
            case Scope.USER:
                return self.user
            case Scope.DEVICE:
                return self.device
            case Scope.GROUP:
                return self.group
            case Scope.VENDOR:
                return None
                # TODO: maybe return Vendor name here?
