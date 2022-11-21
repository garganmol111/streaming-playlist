from django.urls import path

from streaming_playlist.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
    UserFavouritesView,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
    path(
        "favourites/",
        view=UserFavouritesView.as_view(),
        name="favourites",
    ),
]
