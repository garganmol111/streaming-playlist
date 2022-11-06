from django.contrib.auth import get_user_model
from django.urls import reverse
from django.views import View
from django.template import loader
from django.http import HttpResponse

from tmdbv3api import Movie, TV, Episode, Configuration
import json


class MovieView(View):
    def get(self, request, *args, **kwargs):
        config = Configuration().info()

        tmdb_movie = Movie()
        content_id = kwargs["content_id"]
        movie = tmdb_movie.details(content_id)

        image_base_url = config.images.secure_base_url
        image_size = config.images.poster_sizes[1]

        trailer = "#"
        try:
            for vid in movie.trailers.youtube:
                trailer = f"https://www.youtube.com/watch?v={vid.source}"
        except:
            pass

        cast = []

        for actor in movie.casts.cast:
            cast.append(
                {
                    "name": actor.name,
                    "id": actor.id,
                    "photo": f"{image_base_url}{image_size}/{actor.profile_path}",
                    "plays_character": actor.character,
                }
            )

        director = {"name": "N/A", "id": None}
        writers = []
        for crew in movie.casts.crew:
            if crew["job"] == "Director":
                director["name"] = crew["name"]
                director["id"] = crew["id"]

            if crew["job"] == "Writer":
                writers.append({"name": crew["name"], "id": crew["id"]})

        keywords = [i["name"] for i in movie.keywords.keywords]

        watch_providers = []
        try:
            for provider in tmdb_movie.watch_providers(movie.id).results.IN.flatrate:
                watch_providers.append(
                    {
                        "logo_path": provider.logo_path,
                        "provider_name": provider.provider_name,
                    }
                )
            if len(watch_providers) == 0:
                watch_providers = None
        except:
            watch_providers = None
        related_movies = []
        try:
            for similar_movie in tmdb_movie.similar(movie.id):
                related_movies.append(
                    {
                        "title": similar_movie.title,
                        "year": similar_movie.release_date.split("-")[0],
                        "rating": similar_movie.vote_average,
                        "poster": f"{image_base_url}{image_size}/{similar_movie.poster_path}",
                    }
                )

        except:
            related_movies = []

        context = {
            "title": movie.title,
            "year": movie.release_date.split("-")[0],
            "release_date": movie.release_date,
            "poster": f"{image_base_url}{image_size}/{movie.poster_path}",
            "backdrop": f"{image_base_url}{image_size}/{movie.backdrop_path}",
            "overview": movie.overview,
            "genres": movie.genres,
            "rating": movie.vote_average,
            "rating_user_count": movie.vote_count,
            "trailer": trailer,
            "cast": cast,
            "director": director,
            "writers": writers,
            "stars": cast[0:4],
            "runtime": f"{movie.runtime} mins",
            "keywords": keywords,
            "watch_providers": watch_providers,
            "related_movies": related_movies,
        }
        # import pdb

        # pdb.set_trace()

        template = loader.get_template("pages/movie_page.html")
        return HttpResponse(template.render(context, request))


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
