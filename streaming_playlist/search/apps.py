from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SearchConfig(AppConfig):
    name = "streaming_playlist.search"
    verbose_name = _("Search")

    def ready(self):
        try:
            import streaming_playlist.search.signals  # noqa F401
        except ImportError:
            pass
