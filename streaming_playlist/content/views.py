import json

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse
from django.views import View
from tmdbv3api import TV, Configuration, Episode, Movie, Season

from . import utils


class MovieView(View):
    def get(self, request, *args, **kwargs):
        content_id = kwargs["content_id"]

        context = utils.get_movie_info(content_id)

        template = loader.get_template("pages/movie_page.html")
        return HttpResponse(template.render(context, request))


class TVView(View):
    def get(self, request, *args, **kwargs):
        content_id = kwargs["content_id"]

        context = utils.get_tv_info(content_id)

        template = loader.get_template("pages/series_page.html")
        return HttpResponse(template.render(context, request))


class TVSeasonView(View):
    def get(self, request, *args, **kwargs):
        tv_id = kwargs["tv_id"]
        season_number = kwargs["season_number"]

        context = utils.get_season_info(tv_id, season_number)
        template = loader.get_template("pages/season_page.html")
        return HttpResponse(template.render(context, request))


class TVEpisodeView(View):
    def get(self, request, *args, **kwargs):
        tv_id = kwargs["tv_id"]
        season_number = kwargs["season_number"]
        episode_number = kwargs["episode_number"]

        context = utils.get_episode_info(tv_id, season_number, episode_number)
        template = loader.get_template("pages/episode_page.html")
        return HttpResponse(template.render(context, request))
