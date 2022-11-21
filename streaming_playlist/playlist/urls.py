from django.urls import path

from streaming_playlist.playlist.views import (
    PlaylistCreateView,
    PlaylistDeleteView,
    PlaylistDetailView,
    PlaylistListView,
    PlaylistContentDeleteView,
    PlaylistContentCreateView,
)

app_name = "playlist"


urlpatterns = [
    path("", view=PlaylistListView.as_view(), name="list_playlist"),
    path("create/", view=PlaylistCreateView.as_view(), name="create_playlist"),
    path("<int:pk>/", view=PlaylistDetailView.as_view(), name="get_playlist"),
    path(
        "<int:pk>/delete/",
        view=PlaylistDeleteView.as_view(),
        name="delete_playlist",
    ),
    path(
        "deleteEntry/<int:pk>/",
        view=PlaylistContentDeleteView.as_view(),
        name="delete_playlist_entry",
    ),
    path(
        "add-to-playlist/",
        view=PlaylistContentCreateView.as_view(),
        name="add_playlist_entry",
    ),
]
