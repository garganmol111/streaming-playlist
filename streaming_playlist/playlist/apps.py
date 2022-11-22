from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PlaylistConfig(AppConfig):
    name = "streaming_playlist.playlist"
    verbose_name = _("Playlist")

    def ready(self):
        try:
            import streaming_playlist.playlist.signals  # noqa F401
        except ImportError:
            pass
