from django.contrib.auth import get_user_model
from django.urls import reverse
from django.views import View
from django.template import loader
from django.http import HttpResponse

from tmdbv3api import Movie, TV, Episode
import json


class MovieView(View):
    def get(self, request, *args, **kwargs):
        tmdb_movie = Movie()
        content_id = kwargs["content_id"]
        movie = tmdb_movie.details(content_id)

        template = loader.get_template("pages/movie_page.html")
        return HttpResponse(template.render({}, request))


class TVView(View):
    def get(self, request, *args, **kwargs):
        tmdb_tv = TV()
        content_id = kwargs["content_id"]
        tv = tmdb_tv.details(content_id)


class TVEpisodeView(View):
    def get(self, request, *args, **kwargs):
        tmdb_episode = Episode()
        content_id = kwargs["content_id"]
        episode = tmdb_episode.details(content_id)
