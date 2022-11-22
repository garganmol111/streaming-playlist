from django.urls import path

from streaming_playlist.home.views import HomeView

app_name = "home"
urlpatterns = [
    path("", view=HomeView.as_view(), name="homepage"),
]
