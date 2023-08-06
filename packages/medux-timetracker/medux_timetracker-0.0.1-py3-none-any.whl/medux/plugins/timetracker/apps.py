from django.utils.translation import gettext_lazy as _

from gdaps.api import require_app

# from gdaps.frontend.conf import frontend_settings
from . import __version__
from medux.common.api import MeduxPluginAppConfig


class TimetrackerConfig(MeduxPluginAppConfig):
    """A GDAPS Django app plugin.

    It needs a special parameter named ``PluginMeta``. It is the key for GDAPS
    to recognize this app as a GDAPS plugin.
    ``PluginMeta`` must point to a class that implements certain attributes
    and methods.
    """

    name = "medux.plugins.timetracker"

    groups_permissions = {
        "Users": {
            "timetracker.TimeEntry": ["view", "add", "change", "delete"],
            "timetracker.Holiday": ["view", "add", "change", "delete"],
        },
        "Holiday admins": {"timetracker.Holiday": ["administer"]},
    }

    class PluginMeta:
        """This configuration is the introspection data for plugins."""

        # the plugin machine "name" is taken from the AppConfig, so no name here
        verbose_name = _("Timetracker")
        author = "Christian González"
        author_email = "office@nerdocs.at"
        vendor = "Nerdocs"
        description = _("Timetracking for employees")
        category = _("Base")
        visible = True
        version = __version__
        # compatibility = "medux.core>=2.3.0"

    def ready(self):
        # This function is called after the app and all models are loaded.
        #
        # You can do some initialization here, but beware: it should rather
        # return fast, as it is called at each Django start, even on
        # management commands (makemigrations/migrate etc.).
        #
        # Avoid interacting with the database especially 'save' operations,
        # if you don't *really* have to."""

        try:
            from . import signals
        except ImportError:
            pass

        require_app(self, "medux")
