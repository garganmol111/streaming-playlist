from django.urls import path

from streaming_playlist.search.views import SearchView

app_name = "search"
urlpatterns = [
    path("", view=SearchView.as_view(), name="search_content"),
]
