from django.utils.translation import gettext_lazy
from . import __version__

try:
    from pretix.base.plugins import PluginConfig
except ImportError:
    raise RuntimeError("Please use pretix 2.7 or above to run this plugin!")


class PluginApp(PluginConfig):
    default = True
    name = "pretix_dob_validation"
    verbose_name = "Date of Birth Validation"

    class PretixPluginMeta:
        name = gettext_lazy("Date of Birth Validation")
        author = "pretix team"
        description = gettext_lazy("Allows to add date of birth validation to date questions")
        visible = True
        version = __version__
        category = "CUSTOMIZATION"
        compatibility = "pretix>=3.18.0.dev0"

    def ready(self):
        from . import signals  # NOQA

