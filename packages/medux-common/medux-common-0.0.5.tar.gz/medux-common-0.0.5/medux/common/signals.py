from django.contrib.auth import get_user_model

from .constants import USERS_GROUP_NAME


def add_user_to_users_group(sender, instance, **kwargs):
    """Signal receiver that is called after each creation of a User
    and adds this user to the "Users" group.
    """
    from django.contrib.auth.models import Group

    User = get_user_model()

    if not sender == User:
        return

    users_group, created = Group.objects.get_or_create(name=USERS_GROUP_NAME)
    if created:
        users_group.save()

    # add "Users" group to user's groups
    instance.groups.add(users_group)
