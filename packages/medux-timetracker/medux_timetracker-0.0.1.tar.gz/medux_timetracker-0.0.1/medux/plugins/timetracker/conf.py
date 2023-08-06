from django.test.signals import setting_changed
from gdaps.conf import PluginSettings

# This is a default conf file for a GDAPS plugin.
# You can use settings anywhere in your plugin using this syntax:
#
#     from .conf import timetracker_settings
#     # or:
#     # from /home/christian/Projekte/timetracker_dev/medux/plugins.timetracker.conf import timetracker_settings
#
#     foo = timetracker_settings.FOO_SETTING
#
# This way you can use custom (plugin-default) settings, that can be overridden globally if needed.


# required parameter.
NAMESPACE = 'TIMETRACKER'

# Optional defaults. Leave empty if not needed.
DEFAULTS = {
    # 'MY_SETTING': 'somevalue',
    # 'FOO_PATH': '/home/christian/Projekte/timetracker_dev/medux/plugins.timetracker.models.FooModel',
    # 'BAR': [
    #     'baz',
    #     'buh',
    # ],
}

# Optional list of settings keys that are allowed to be in 'string import' notation. Leave empty if not needed.
IMPORT_STRINGS = (
    # 'FOO_PATH',
)

# Optional list of settings that have been removed. Leave empty if not needed.
REMOVED_SETTINGS = ()


timetracker_settings = PluginSettings(NAMESPACE, DEFAULTS, IMPORT_STRINGS)


def reload_timetracker_settings(*args, **kwargs):
    setting = kwargs['setting']
    if setting == 'TIMETRACKER':
        timetracker_settings.reload()


setting_changed.connect(reload_timetracker_settings)
