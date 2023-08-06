from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _

from . import __version__
from medux.common.api import MeduxPluginAppConfig


class CommonConfig(MeduxPluginAppConfig):
    """A GDAPS Django app plugin.

    It needs a special parameter named ``PluginMeta``. It is the key for GDAPS
    to recognize this app as a GDAPS plugin.
    ``PluginMeta`` must point to a class that implements certain attributes
    and methods.
    """

    name = "medux.common"
    # greate empty users group
    groups_permissions = {"Users": {}}

    class PluginMeta:
        """This configuration is the introspection data for plugins."""

        # the plugin machine "name" is taken from the AppConfig, so no name here
        verbose_name = _("Common")
        author = "Christian González"
        author_email = "office@nerdocs.at"
        vendor = "Nerdocs"
        description = _(
            "MedUX common tools and models, which are used for medux_online and medux"
        )
        category = _("Base")
        visible = True
        version = __version__
        # compatibility = "medux.core>=2.3.0"

    def initialize(self):
        pass

    def ready(self):
        from . import signals

        post_save.connect(signals.add_user_to_users_group, sender=get_user_model())
