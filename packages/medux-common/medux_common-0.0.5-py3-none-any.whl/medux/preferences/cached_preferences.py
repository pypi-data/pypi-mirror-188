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
from django.contrib.auth.models import Group
from django.db import models

from medux.common.models import Tenant
from medux.preferences.definitions import KeyType, Scope
from medux.preferences.models import ScopedPreference, BasePreference
from medux.preferences.registry import PreferencesRegistry
from medux.preferences.tools import get_effective_setting


class CachedPreferences:
    """Creates a request specific set of preferences, usable for templates.

    CachedPreferences allows easy access to the preferences for a specific context, given a request:

    CachedPreferences(request).my_namespace.my_setting returns the specific setting. It respects the current
    user, groups, device, and tenant

    # It creates a dict with nested preferences:
    # <namespace>
    # +-<key-1>
    #   +-user
    #   | +- value: 1
    #   | +- user: 23
    #   +-device
    #     +- value: 2
    #     +- device: 23543
    # ...
    """

    from django.http import HttpRequest

    class Namespace:
        """Transparently represents the first part (=namespace, before the dot) of a key, when
        accessed as CachedPreferences' attribute, e.g.
        ```python
        preferences = CachedPreferences(request)
        preferences.prescriptions.medication_message
        ```
        """

        from django.http import HttpRequest

        def __init__(self, request: HttpRequest, namespace: str):
            self.namespace = namespace
            self.request = request

        def __repr__(self):
            return f"<Namespace '{self.namespace}'>"

        def __getattr__(self, key: str) -> str | None:
            """get a list of preferences items with that key, ordered by scope:

            The scope order is: USER > DEVICE > GROUP > TENANT > VENDOR
            If a key is found during the traversal, its value is returned, else the next scope is
            looked up. If no key is found, None is returned.
            """

            setting = get_effective_setting(
                namespace=self.namespace,
                key=key,
                request=self.request,
            )
            # special case boolean.False, or None: return "" for  template variables
            if setting.key_type == KeyType.BOOLEAN and setting.value.lower() == "false":
                return ""
                # FIXME: this should be done better, distinguish between template and view code

            return setting.value

    def __init__(self, request: HttpRequest):

        self.request = request

    def __getattr__(self, namespace):
        """Helper to retrieve preferences key (all scopes) in a pythonic way:

        CachedPreferences.<namespace>.<key>"""

        return self.Namespace(self.request, namespace)

    @classmethod
    def get(
        cls,
        namespace: str,
        key: str,
        scope: Scope,
        full_object: bool = False,
        user=None,
        group: Group | None = None,
        device=None,  # TODO add device support
        tenant: Tenant | None = None,
    ) -> int | str | bool | models.Model | None:
        """Convenience method to retrieve a preferences key.

        :return: namespaced preferences value, according to given scope
            and, if applicable, the related object like user, group etc.
            If no object exists, return None.
            If pointing to an unregistered namespace/key, raise a
            KeyError.

        :param namespace: the namespace this key is saved under.
            Usually the app's name.
        :param key: the key to be retrieved
        :param scope: the scope that key is valid for. If scope is None,
            and more than one keys are saved under that scope, the key
            with the highest priority is taken:
            USER > DEVICE > GROUP > TENANT > VENDOR
        :param key_type: preferences type: "str", "bool", "int"
        :param full_object: if True, return the complete model instance
            instead of only its value
        :param user: if scope is USER, you have to provide a User object
            that key/scope is valid for.
        :param group: if scope is GROUP, you have to provide a
            SettingsGroup object that key/scope is valid for.
        :param device: if scope is DEVICE, you have to provide a Device
            object that key/scope is valid for.
        :param tenant: if scope is TENANT, you have to provide a Tenant
            object that key/scope is valid for.
        """

        ScopedPreference.assure_exists(namespace, key, scope)
        key_type = PreferencesRegistry.key_type(namespace, key)

        filters = {
            "base__namespace": namespace,
            "base__key": key,
        }
        if scope:
            filters["scope"] = scope
            if scope == Scope.USER:
                filters["user"] = user
            elif scope == Scope.GROUP:
                filters["group"] = group
            elif scope == Scope.DEVICE:
                filters["device"] = device
            elif scope == Scope.TENANT:
                filters["tenant"] = tenant

        objects = ScopedPreference.objects.filter(**filters)
        if len(objects) == 0:
            # if this setting does not exist (yet), return None
            return None

        if len(objects) == 1:
            obj = objects.first()
            if full_object:
                return obj
            value = obj.value  # type: str
        else:
            # more than one scopes under that key and scope
            ids = ",".join(i.id for i in objects)
            raise KeyError(
                f"There are multiple preferences keys under {namespace}.{key}[{scope}]: ids {ids}"
            )
        # filter out int and boolean values and return them instead.
        if key_type == KeyType.INTEGER:
            return int(value)
        if key_type == KeyType.BOOLEAN:
            if value.lower() == "false":
                return False
            elif value.lower() == "true":
                return True
            else:
                raise ValueError(f"DB value '{value}' cannot be casted into boolean!")
        if key_type in (KeyType.STRING, KeyType.TEXT):
            return str(value)

        # should never happen...
        raise KeyError(f"Unknown preferences type: {key_type}")

    @classmethod
    def set(
        cls,
        namespace: str,
        key: str,
        value: str | int | bool,
        scope: Scope,
        user=None,
        tenant=None,
        device=None,
        group: Group = None,
    ) -> None:

        """Convenience method to set a preferences key.

        Raises a TypeError if value is of incorrect KeyType
        """

        ScopedPreference.assure_exists(namespace, key, scope)

        # key_type is not used directly, as the value in the DB always is casted to a str.
        # Retrieving later is casted by the type saved in the PreferencesRegistry.

        key_type = PreferencesRegistry.key_type(namespace, key)
        if key_type == KeyType.INTEGER:
            # try to cast value into an integer. If not possible,
            # an Exception is raised.
            int(value)
        elif key_type == KeyType.BOOLEAN:
            if value not in (True, False):
                raise TypeError("value must be a Boolean.")

        filter = {
            "scope": scope,
        }
        # set correct scope
        if scope == Scope.USER:
            if user is None:
                raise AttributeError(
                    "When scope==USER, a user object must be provided."
                )
            filter["user"] = user

        elif scope == Scope.DEVICE:
            if device is None:
                raise AttributeError(
                    "When scope==DEVICE, a device object must be provided."
                )
            filter["device"] = device

        elif scope == Scope.GROUP:
            if group is None:
                raise AttributeError(
                    "When scope==GROUP, a group object must be provided."
                )
            filter["group"] = group

        elif scope == Scope.TENANT:
            if tenant is None:
                raise AttributeError(
                    "When scope==TENANT, a tenant object must be provided."
                )
            filter["tenant"] = tenant

        # TODO: maybe do some casting / checks here?

        # if base setting does not exist, create it
        base, base_created = BasePreference.objects.get_or_create(
            namespace=namespace, key=key
        )
        if base_created:
            base.save()
        filter["base"] = base

        # get_or_create can't be used, as old / new value could differ,
        # so get() must not include it.
        try:
            item = ScopedPreference.objects.get(**filter)
        except ScopedPreference.DoesNotExist:
            filter["value"] = value
            item = ScopedPreference.objects.create(**filter)

        item.value = str(value)
        item.save()


# @receiver(request_finished)
# def on_request_finished(sender, **kwargs):
#     preferences.invalidate()
