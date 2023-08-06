import logging

import toml
from django.db import transaction

from medux.preferences.cached_preferences import CachedPreferences
from medux.preferences.definitions import Scope
from medux.preferences.models import ScopedPreference
from medux.preferences.registry import PreferencesRegistry

logger = logging.getLogger(__file__)


class PreferencesLoader:
    """Base for Preferences loaders.

    You have to provide a Scope where this preferences go into (defaults to VENDOR)
    """

    def __init__(self, scope: Scope = Scope.VENDOR, foreign_object=None):
        # FIXME: change foreign_object to user/tenant/etc.?
        self.scope = scope
        if scope == scope.VENDOR:
            self.foreign_object = {}
        else:
            self.foreign_object = {scope.name.lower(): foreign_object}

    def load(self):
        """load the preferences file"""
        raise NotImplementedError

    def save(self):
        raise NotImplementedError

    def update_preferences(self, dct):
        """Updates the preferences using a dict:
        {
            "namespace_a":
                "let_user_decide": True,
                "other_preference": 42,
            },
            "namespace_b": {...}
        }
        """
        # wrong_keys = []
        with transaction.atomic():
            for namespace, keys in dct.items():
                for key in keys:
                    # allow not settin that is not registered
                    if not PreferencesRegistry.exists(namespace, key, self.scope):
                        raise KeyError(
                            f"Key {namespace}.{key} is not registered and can't be imported. Please register first."
                        )
                    CachedPreferences.set(
                        namespace=namespace,
                        key=key,
                        scope=self.scope,
                        value=dct[namespace][key],
                        **self.foreign_object,
                    )  # type: ScopedPreference


class TomlPreferencesLoader(PreferencesLoader):
    def __init__(self, filename, scope: Scope = Scope.VENDOR, foreign_object=None):
        super().__init__(scope, foreign_object)
        self._filename = filename

    def load(self):
        try:
            with open(self._filename, "r") as f:
                self.update_preferences(toml.load(f))
        except FileNotFoundError:
            raise
        except toml.TomlDecodeError as e:
            logger.error(f"Could load load file {self._filename}: {e}")


# TODO make non-VENDOR bulk-updates work
