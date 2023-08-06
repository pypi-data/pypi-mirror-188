from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
from gdaps.pluginmanager import PluginManager

from . import __version__
from medux.common.api import MeduxPluginAppConfig


class CoreConfig(MeduxPluginAppConfig):
    """MedUX Core Plugin"""

    default_auto_field = "django.db.models.BigAutoField"
    default = True  # FIXME: Remove when django bug is fixed
    name = "medux.core"
    groups_permissions = {
        "Users": {"core.Patient": ["view"]},
        "Patient managers": {"core.Patient": ["add", "change", "delete"]},
    }

    class PluginMeta:
        verbose_name = _("MedUX Core")
        author = "Christian González"
        author_email = "christian.gonzalez@nerdocs.at"
        vendor = "nerdocs"
        description = _("Medux Core Plugin")
        category = _("Core")
        visible = True
        version = __version__

    def ready(self):
        # This function is called after the app and all models are loaded.
        #
        # You can do some initialization here, but beware: it should rather
        # return fast, as it is called at each Django start, even on
        # management commands (makemigrations/migrate etc.).
        #
        # Avoid interacting with the database especially 'save' operations,
        # if you don't *really* have to."""

        from . import signals

        # post_save.connect()

        # load all components and menus
        PluginManager.load_plugin_submodule("menus")
