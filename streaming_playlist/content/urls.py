from django.urls import path

from streaming_playlist.content.views import (
    MovieView,
    TVView,
    TVSeasonView,
    TVEpisodeView,
)

app_name = "content"
urlpatterns = [
    # get movie details
    path("movie/<str:content_id>/", view=MovieView.as_view(), name="get_movie"),
    # get tv series details
    path("tv/<str:content_id>/", view=TVView.as_view(), name="get_tv"),
    # get tv season details
    path(
        "tv/<str:tv_id>/season/<season_number>/",
        view=TVSeasonView.as_view(),
        name="get_season",
    ),
    # get tv episode details
    path(
        "tv/<str:tv_id>/season/<season_number>/episode/<str:episode_number>/",
        view=TVEpisodeView.as_view(),
        name="get_episode",
    ),
]
