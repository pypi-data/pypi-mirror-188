from django.test import TestCase

from medux.common.tools import create_groups_permissions

groups_permissions = {
    "Site tester": {
        "core.TermsAndConditionsPage": ["view", "add", "change", "delete"],
        "core.PrivacyPage": ["view", "add", "change"],
    },
    # "Site admins": {
    #     "core.TermsAndConditionsPage": ["view", "add", "change", "delete"],
    #     "core.PrivacyPage": ["view", "add", "change", "delete"],
    # },
}


class TestPermissionsCreation(TestCase):
    def test_correct_permissions(self):
        create_groups_permissions(
            {"group1": {"core.User": ["view", "add", "change", "delete"]}}
        )

    def test_add_permissions_to_existing_group(self):
        create_groups_permissions({"group2": {"core.User": ["view", "add", "change"]}})
        create_groups_permissions({"group2": {"core.User": ["delete"]}})

    def test_add_permissions_to_nonexisting_model(self):
        with self.assertRaises(LookupError):
            create_groups_permissions(
                {"group3": {"common.XYZ_does_not_exist": ["view", "add", "change"]}}
            )
