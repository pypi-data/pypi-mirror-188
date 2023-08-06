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
import logging

from django.utils.translation import gettext_lazy as _

from medux.common.api import MeduxPluginAppConfig
from . import __version__

logger = logging.getLogger(__file__)


class PreferencesConfig(MeduxPluginAppConfig):
    name = "medux.preferences"
    verbose_name = _("Preferences")
    default = True  # FIXME: Remove when django bug is fixed
    groups_permissions = {
        "Users": {"preferences.ScopedPreference": ["view", "change_own_user"]},
        "Tenant admins": {"preferences.ScopedPreference": ["change_own_tenant"]},
    }

    class PluginMeta:
        """This configuration is the introspection data for plugins."""

        # the plugin machine "name" is taken from the AppConfig, so no name here
        verbose_name = _("Preferences")
        author = "Christian González"
        author_email = "office@nerdocs.at"
        vendor = "Nerdocs"
        description = _(
            "MedUX preferences tools, which are used for MedUX Online and MedUX"
        )
        category = _("Base")
        visible = True
        version = __version__

    # compatibility = "medux.core>=2.3.0"
