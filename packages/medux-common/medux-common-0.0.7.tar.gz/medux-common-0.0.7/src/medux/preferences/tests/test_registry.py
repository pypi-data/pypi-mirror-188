from unittest import TestCase

from medux.preferences.definitions import Scope, KeyType
from medux.preferences.registry import PreferencesRegistry


class TestRegistry(TestCase):
    def test_register_key(self):
        PreferencesRegistry.register("namespace", "key1", [Scope.USER, Scope.VENDOR])
        self.assertTrue(PreferencesRegistry.exists("namespace", "key1", Scope.USER))

    def test_register_wrong_key(self):
        PreferencesRegistry.register("namespace", "key2", [Scope.USER, Scope.VENDOR])
        self.assertFalse(PreferencesRegistry.exists("namespace", "key33", Scope.USER))

    def test_register_wrong_namespace(self):
        PreferencesRegistry.register("namespace", "key3", [Scope.USER, Scope.VENDOR])
        self.assertFalse(PreferencesRegistry.exists("foospace", "key45", Scope.USER))

    def test_register_wrong_scope(self):
        PreferencesRegistry.register("namespace", "key4", [Scope.USER, Scope.VENDOR])
        self.assertFalse(PreferencesRegistry.exists("namespace", "key4", Scope.DEVICE))

    def test_register_implicitly_vendor_scope(self):
        """check if registered settings add VENDOR scope automatically"""
        PreferencesRegistry.register("namespace", "key5", [Scope.USER])
        self.assertTrue(PreferencesRegistry.exists("namespace", "key5", Scope.VENDOR))

    def test_retrieve_scopes(self):
        PreferencesRegistry.register("namespace", "key6", [Scope.USER, Scope.DEVICE])
        self.assertEqual(
            PreferencesRegistry.scopes("namespace", "key6"),
            {
                Scope.USER,
                Scope.DEVICE,
                Scope.VENDOR,
            },
        )

    def test_retrieve_empty_scopes(self):
        PreferencesRegistry.register("namespace", "key_empty", [])
        self.assertEqual(
            PreferencesRegistry.scopes("namespace", "key_empty"), {Scope.VENDOR}
        )

    def test_retrieve_vendor_scopes(self):
        PreferencesRegistry.register("namespace", "key_vendor", [Scope.VENDOR])
        self.assertEqual(
            PreferencesRegistry.scopes("namespace", "key_vendor"), {Scope.VENDOR}
        )

    def test_all(self):
        PreferencesRegistry.register(
            "namespace", "key_vendor", [Scope.VENDOR], key_type=KeyType.INTEGER
        )
        PreferencesRegistry.register("namespace2", "key_user", [Scope.USER])
        result = list(PreferencesRegistry.all())
        # self.assertEqual(len(result), 3)
        self.assertIn(
            ("namespace", "key_vendor", Scope.VENDOR, KeyType.INTEGER), result
        )
        self.assertIn(("namespace2", "key_user", Scope.VENDOR, KeyType.STRING), result)
        self.assertIn(("namespace2", "key_user", Scope.USER, KeyType.STRING), result)
