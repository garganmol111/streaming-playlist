from django.contrib.auth import get_user_model
from django.urls import reverse
from django.views import View
from django.template import loader
from django.http import HttpResponse

from tmdbv3api import Movie, TV, Episode, Configuration
import json


class HomeView(View):
    def get(self, request, *args, **kwargs):

        config = Configuration().info()
        movie = Movie()
        tv = TV()

        poster_base_url = config.images.secure_base_url
        poster_size = config.images.poster_sizes[1]

        trending_movies = []
        trending_tv = []

        for m in movie.popular():
            trending_movies.append(
                {
                    "id": m.id,
                    "title": m.title,
                    "poster": f"{poster_base_url}{poster_size}/{m.poster_path}",
                    "year": m.release_date.split("-")[0],
                    "rating": m.vote_average,
                }
            )

        for t in tv.popular():

            trending_tv.append(
                {
                    "id": t.id,
                    "title": t.name,
                    "poster": f"{poster_base_url}{poster_size}/{t.poster_path}",
                    "year": t.first_air_date.split("-")[0],
                    "rating": t.vote_average,
                }
            )

        context = {
            "trending_movies": trending_movies,
            "trending_tv": trending_tv,
        }

        template = loader.get_template("pages/home.html")
        return HttpResponse(template.render(context, request))
