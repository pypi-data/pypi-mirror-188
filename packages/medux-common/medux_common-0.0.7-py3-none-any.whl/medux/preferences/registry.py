import logging

from medux.preferences.definitions import KeyType, Scope

logger = logging.getLogger(__file__)


class PreferencesRegistry:
    """A in-memory storage where preferences namespaces/keys/scopes are registered at
    application start and can be checked against for existence and type.

    Every available setting *must* be registered before usage.

    You can add a (translatable) help_text and an icon to each key here,
    which can be retrieved from the setting itself later.
    """

    # namespace, key, scope
    _registered_keys: list[tuple[str, str, Scope, str]] = []
    _key_types: dict[tuple[str, str], KeyType] = {}
    _help_texts: dict[tuple[str, str], str] = {}
    _icons: dict[tuple[str, str], str] = {}

    def __init__(self):
        raise NotImplementedError(
            f"{self.__class__.__name__} is not meant to be instantiated."
        )

    @classmethod
    def register(
        cls,
        namespace: str,
        key: str,
        allowed_scopes: list["Scope"] = None,
        key_type: KeyType = KeyType.STRING,
        help_text: str = "",
        icon: str = "gear",
    ):
        """Registers a preferences variable in a global list.

        This makes sure that preferences variables read in from e.g. .toml files can only be accepted if they
        match existing, already registered preferences.
        :param namespace: The namespace of the key
        :param key: the key name
        :param allowed_scopes: a list of allowed `Scope`s. VENDOR will be added automatically.
        :param key_type: the type of the setting. Other types are not allowed at assignment later.
        :param help_text: the (translatable) help text that explains in short words what this setting is for
        :param icon: the Bootstrap5 icon used for this setting
        """

        # VENDOR scope is always allowed
        if allowed_scopes is None:
            allowed_scopes = []
        if Scope.VENDOR not in allowed_scopes:
            allowed_scopes.append(Scope.VENDOR)

        cls._help_texts[(namespace, key)] = help_text
        for scope in allowed_scopes:
            t = (namespace, key, scope)
            # can't register same key again...
            if t in cls._registered_keys:
                logger.warning(
                    f"Key {namespace}.{key} [{scope.name}] was already registered!"
                )
            else:
                cls._registered_keys.append(t)
                cls._key_types[(namespace, key)] = key_type
                cls._icons[(namespace, key)] = icon

    @classmethod
    def exists(cls, namespace: str, key: str, scope: Scope) -> bool:
        """:return: True if there was a setting with given namespace.key/scope registered."""

        # return (namespace, key, scope) in cls._registered_keys
        return (namespace, key, scope) in cls._registered_keys

    @classmethod
    def scopes(cls, namespace: str, key: str) -> set[Scope]:
        """:return: a set of scopes registered under the given namespaced preferences key."""
        scopes = set()
        for s in cls._registered_keys:
            if s[0] == namespace and s[1] == key:
                scopes.add(s[2])
        return scopes

    @classmethod
    def key_type(cls, namespace: str, key: str) -> KeyType:
        """:return: the type of the given namespaced preferences key."""
        t = (namespace, key)
        if t in cls._key_types:
            return cls._key_types[t]
        else:
            raise KeyError(f"No setting '{namespace}.{key}' registered.")

    @classmethod
    def all_dct(cls) -> dict[str, dict[str, str]]:
        _all = {}
        for namespace, key, scope in cls._registered_keys:
            if namespace not in _all:
                _all[namespace] = {}
            if key not in _all[namespace]:
                _all[namespace][key] = {}

            _all[namespace][key][scope] = ""
        return _all

    @classmethod
    def all(cls) -> tuple[str, str, str, str]:
        """:return: A tuple of all registered preferences keys: namespace, key, scope, key_type"""
        for setting_tuple in cls._registered_keys:
            yield setting_tuple + (cls._key_types[setting_tuple[0:2]],)

    @classmethod
    def help_text(cls, namespace: str, key: str) -> str:
        return cls._help_texts[(namespace, key)]

    @classmethod
    def icon(cls, namespace: str, key: str) -> str:
        """:return: The Boostrap5 icon name of this setting."""
        return cls._icons[(namespace, key)]

    def delete_orphaned_preferences(cls):
        """Finds orphaned keys and deletes them.

        Orphaned preferences whose Registry key was deleted during
        evolvement of MedUX still stay in the database and may produce
        problems.
        This procedure deletes every setting that is not registered
         in the PreferencesRegistry any more.
        """
        from .models import ScopedPreference

        orphaned_ids = []
        for item in ScopedPreference.objects.all():
            if not PreferencesRegistry.exists(item.namespace, item.key, item.scope):
                # FIXME: take care of "orphaned" keys which are bound to a user, device, or tenant.
                orphaned_ids.append(item.id)
        ScopedPreference.objects.filter(id__in=orphaned_ids).delete()
