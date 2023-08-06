import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from medux.preferences.cached_preferences import CachedPreferences
from medux.preferences.definitions import Scope, KeyType
from medux.preferences.models import ScopedPreference
from medux.preferences.registry import PreferencesRegistry


@pytest.fixture
def user_admin():
    admin = get_user_model().objects.create(username="admin")
    admin.save()
    return admin


@pytest.fixture
def user_nobody():
    nobody = get_user_model().objects.create(username="nobody")
    nobody.save()
    return nobody


@pytest.fixture
def dummy_group():
    group = Group.objects.create(name="dummy")
    group.save()
    return group


@pytest.mark.django_db
def test_preferences_get_nonexisting():
    """test if non-existing setting returns None"""
    PreferencesRegistry.register("test", "non_existing", [Scope.VENDOR])
    result = CachedPreferences.get("test", "non_existing", Scope.VENDOR)
    assert result is None


@pytest.mark.django_db
def test_preferences_integer(user_admin, user_nobody):
    """test if an int preferences returns actually an int"""
    PreferencesRegistry.register(
        "test", "int_setting", [Scope.USER], key_type=KeyType.INTEGER
    )
    ScopedPreference.set(
        "test",
        "int_preferences",
        42,
        Scope.USER,
        user=user_admin,
    )

    result = CachedPreferences.get(
        "test", "int_preferences", Scope.USER, user=user_admin
    )
    assert result == 42
    assert type(result) == int

    result = CachedPreferences.get(
        "test", "int_preferences", Scope.USER, user=user_nobody
    )
    assert result is None


@pytest.mark.django_db
def test_spreferences_integer_casting(admin_user):
    """test if an int preferences returns actually an int"""
    PreferencesRegistry.register(
        "test", "cast_int_preferences", [Scope.USER], key_type=KeyType.INTEGER
    )
    ScopedPreference.set(
        "test", "cast_int_preferences", "42", Scope.USER, user=admin_user
    )

    assert (
        CachedPreferences.get(
            "test", "cast_int_preferences", Scope.USER, user=admin_user
        )
        == 42
    )


@pytest.mark.django_db
def test_preferences_str(admin_user):
    """test if a str preferences actually returns a str"""
    PreferencesRegistry.register(
        "test", "str_setting", [Scope.USER], key_type=KeyType.STRING
    )
    ScopedPreference.set("test", "str_preferences", "42a", Scope.USER, user=admin_user)

    assert (
        CachedPreferences.get("test", "str_preferences", Scope.USER, user=admin_user)
        == "42a"
    )


@pytest.mark.django_db
def test_preferences_bool_true(admin_user):
    """test if a bool:True preferences actually returns bool:True"""
    PreferencesRegistry.register(
        "test", "true_preferences", [Scope.USER], key_type=KeyType.BOOLEAN
    )
    ScopedPreference.set("test", "true_preferences", True, Scope.USER, user=admin_user)
    result = CachedPreferences.get(
        "test", "true_preferences", Scope.USER, user=admin_user
    )
    assert result is True


@pytest.mark.django_db
def test_preferences_bool_false(admin_user):
    """test if a bool:False preferences actually returns bool:False"""
    PreferencesRegistry.register(
        "test", "false_preferences", [Scope.USER], key_type=KeyType.BOOLEAN
    )
    ScopedPreference.set(
        "test", "false_preferences", False, Scope.USER, user=admin_user
    )
    result = CachedPreferences.get(
        "test", "false_preferences", Scope.USER, user=admin_user
    )
    assert result is False


@pytest.mark.django_db
def test_spreferences_set_get_USER(admin_user, user_nobody):
    """test if a USER scoped setting returns the correct user and key"""
    PreferencesRegistry.register(
        "test", "user_preferences", [Scope.USER], key_type=KeyType.STRING
    )
    ScopedPreference.set("test", "user_preferences", "foo", Scope.USER, user=admin_user)

    assert (
        CachedPreferences.get("test", "user_preferences", Scope.USER, user=admin_user)
        == "foo"
    )
    assert (
        CachedPreferences.get("test", "user_preferences", Scope.USER, user=user_nobody)
        is None
    )


@pytest.mark.django_db
def test_preferences_set_get_USER_overwrite(admin_user):
    """test if a USER scoped setting returns the correct user and key"""
    PreferencesRegistry.register(
        "test", "user_preferences", [Scope.USER], key_type=KeyType.STRING
    )
    ScopedPreference.set("test", "user_preferences", "foo", Scope.USER, user=admin_user)
    ScopedPreference.set(
        "test", "user_preferences", "foo2", Scope.USER, user=admin_user
    )

    assert (
        CachedPreferences.get("test", "user_preferences", Scope.USER, user=admin_user)
        == "foo2"
    )


@pytest.mark.django_db
def test_preferences_set_get_VENDOR():
    PreferencesRegistry.register(
        "test", "vendor_preferences", [Scope.VENDOR], key_type=KeyType.STRING
    )
    ScopedPreference.set("test", "vendor_preferences", "shdkjhf", Scope.VENDOR)

    assert (
        CachedPreferences.get("test", "vendor_preferences", Scope.VENDOR) == "shdkjhf"
    )


@pytest.mark.django_db
def test_preferences_set_get_VENDOR_auto_keytype():
    PreferencesRegistry.register("test", "vendor_preferences", [Scope.VENDOR])
    ScopedPreference.set("test", "vendor_preferences", "shdkjhf", Scope.VENDOR)

    assert (
        CachedPreferences.get("test", "vendor_preferences", Scope.VENDOR) == "shdkjhf"
    )


@pytest.mark.django_db
def test_preferencesset_get_default_scope():
    PreferencesRegistry.register(
        "test", "vendor_preference2", [Scope.VENDOR], KeyType.INTEGER
    )
    ScopedPreference.set("test", "vendor_preference2", 42, Scope.VENDOR)

    result = CachedPreferences.get("test", "vendor_preference2", Scope.VENDOR)
    assert result == 42
    pass


@pytest.mark.django_db
def test_preferences_set_get_without_user_fk_object():
    PreferencesRegistry.register(
        "test", "vendor_preferences", [Scope.USER], key_type=KeyType.INTEGER
    )
    with pytest.raises(AttributeError):
        ScopedPreference.set("test", "vendor_preferences", 45, Scope.USER)


@pytest.mark.django_db
def test_preferences_set_get_specific_scope(user_admin, user_nobody, dummy_group):
    """Make sure scope with the highest priority is returned when more than one scopes
    are available for a key"""
    PreferencesRegistry.register(
        "test",
        "multiple_preferences",
        [Scope.VENDOR, Scope.USER, Scope.GROUP],
        key_type=KeyType.INTEGER,
    )
    ScopedPreference.set("test", "multiple_preferences", 42, Scope.VENDOR)
    ScopedPreference.set(
        "test", "multiple_preferences", 43, Scope.USER, user=user_admin
    )
    ScopedPreference.set(
        "test", "multiple_preferences", 52, Scope.GROUP, group=dummy_group
    )  # dummy

    assert (
        CachedPreferences.get(
            "test", "multiple_preferences", Scope.USER, user=user_admin
        )
        == 43
    )
