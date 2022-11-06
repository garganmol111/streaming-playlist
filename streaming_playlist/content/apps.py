from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "streaming_playlist.content"
    verbose_name = _("Content")

    def ready(self):
        try:
            import streaming_playlist.content.signals  # noqa F401
        except ImportError:
            pass
