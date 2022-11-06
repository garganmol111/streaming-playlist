from django.urls import path

from streaming_playlist.content.views import MovieView, TVView, TVEpisodeView

app_name = "content"
urlpatterns = [
    path("movie/<str:content_id>/", view=MovieView.as_view(), name="get_movie"),
    path("tv/<str:content_id>/", view=TVView.as_view(), name="get_tv"),
    path("episode/<str:content_id>/", view=TVEpisodeView.as_view(), name="get_episode"),
]
