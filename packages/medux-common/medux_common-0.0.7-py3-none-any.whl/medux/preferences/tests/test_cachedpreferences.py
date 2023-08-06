from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.http import HttpRequest
from django.test import TestCase
from medux.common.models import Tenant
from medux.preferences.definitions import Scope
from medux.preferences.models import ScopedPreference
from medux.preferences.registry import PreferencesRegistry

User = get_user_model()


class CachedSettings:
    pass


class CachedSettingsTest(TestCase):
    def setUp(self) -> None:
        # create a dummy request
        self.request = HttpRequest()

    def test_cachedpreferences_namespace_type(self):
        namespace = CachedSettings(self.request).mynamespace
        self.assertEqual(type(namespace), CachedSettings.Namespace)

    def test_cachedpreferences_key_None(self):
        key = CachedSettings(self.request).test.non_existing_key
        self.assertIsNone(key)

    def test_cachedpreferences_existing_key_vendor(self):
        PreferencesRegistry.register("space", "my_key")
        ScopedPreference.set("space", "my_key", 42, Scope.VENDOR)
        self.assertEqual(CachedSettings(self.request).space.my_key, 42)

    def test_cachedpreferences_existing_key_tenant(self):
        PreferencesRegistry.register("space", "my_key", [Scope.TENANT])
        tenant = Tenant.objects.create(
            first_name="Demo", last_name="User", sex="f", address="Foo street"
        )
        tenant.save()

        ScopedPreference.set("space", "my_key", 42, Scope.TENANT, tenant=tenant)
        self.request.site = Site.objects.get(pk=1)
        space = CachedSettings(self.request).space
        key = space.my_key
        assert key == 42

    def test_cachedpreferences_existing_key_with_correct_user(self):
        user1 = User.objects.create_user(username="user1", password="user1")
        PreferencesRegistry.register("space", "my_key", [Scope.USER])
        ScopedPreference.set("space", "my_key", 42, Scope.USER, user=user1)
        self.request.user = user1
        self.assertEqual(CachedSettings(self.request).space.my_key, 42)

    def test_cachedpreferences_existing_key_with_wrong_user(self):
        user1 = User.objects.create_user(username="user1", password="user1")
        user2 = User.objects.create_user(username="user2", password="user2")

        ScopedPreference.set("space", "my_key", 42, Scope.USER, user=user1)
        self.request.user = user2
        self.assertIsNotNone(CachedSettings(self.request).space)

        key = CachedSettings(self.request).space.my_key
        self.assertIsNone(key)

    def test_cachedpreferences_existing_key_user_fallback_vendor(self):
        user1 = get_user_model().objects.create(username="user1", password="user1")
        user2 = get_user_model().objects.create(username="user2", password="user2")
        PreferencesRegistry.register("space", "my_key", [Scope.USER])

        ScopedPreference.set("space", "my_key", 41, Scope.VENDOR)
        ScopedPreference.set("space", "my_key", 42, Scope.USER, user=user1)
        self.request.user = user2
        self.assertEqual(CachedSettings(self.request).space.my_key, 41)
