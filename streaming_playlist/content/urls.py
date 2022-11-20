from django.urls import path

from streaming_playlist.content.views import (
    MovieView,
    TVView,
    TVSeasonView,
    TVEpisodeView,
)

app_name = "content"
urlpatterns = [
    path("movie/<str:content_id>/", view=MovieView.as_view(), name="get_movie"),
    path("tv/<str:content_id>/", view=TVView.as_view(), name="get_tv"),
    path(
        "tv/<str:tv_id>/season/<season_number>/",
        view=TVSeasonView.as_view(),
        name="get_season",
    ),
    path(
        "tv/<str:tv_id>/season/<season_number>/episode/<str:episode_number>/",
        view=TVEpisodeView.as_view(),
        name="get_episode",
    ),
]
