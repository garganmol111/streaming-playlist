from django.db import models
from streaming_playlist.users.models import User
from django.utils.timezone import now


class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


CONTENT_TYPES = [
    ("movie", "movie"),
    ("episode", "episode"),
]


class PlaylistContent(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    content = models.CharField(max_length=50)
    episode_num = models.CharField(max_length=50, null=True, blank=True)
    series = models.CharField(max_length=50, null=True, blank=True)
    season = models.CharField(max_length=50, null=True, blank=True)
    content_type = models.CharField(
        max_length=50, choices=CONTENT_TYPES, default="movie"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
