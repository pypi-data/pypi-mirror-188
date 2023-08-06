from django.utils.translation import gettext_lazy, gettext
from . import __version__

try:
    from pretix.base.plugins import PluginConfig
except ImportError:
    raise RuntimeError("Please use pretix 2.7 or above to run this plugin!")


class PluginApp(PluginConfig):
    default = True
    name = "pretix_simple_test_results"
    verbose_name = "Simple Test Results"

    class PretixPluginMeta:
        name = gettext_lazy("Simple Test Results")
        author = "pretix"
        description = gettext_lazy("Simple test result sending")
        visible = True
        version = __version__
        category = "FEATURE"
        compatibility = "pretix>=2.7.0"

    def installed(self, event):
        from pretix.base.models import Question

        event.questions.get_or_create(
            identifier="test_result",
            defaults={
                "question": gettext("Test result"),
                "type": Question.TYPE_TEXT,
                "hidden": True,
            },
        )
        q = event.questions.get_or_create(
            identifier="test_type",
            defaults={
                "question": gettext("Test type"),
                "type": Question.TYPE_CHOICE,
                "hidden": True,
            },
        )[0]
        q.options.get_or_create(answer='unknown')

    def ready(self):
        from . import signals  # NOQA


