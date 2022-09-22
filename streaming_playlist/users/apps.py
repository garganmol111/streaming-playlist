from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "streaming_playlist.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import streaming_playlist.users.signals  # noqa F401
        except ImportError:
            pass
