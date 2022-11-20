import json

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse
from django.views import View
from tmdbv3api import TV, Configuration, Episode, Movie, Season


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
                        "id": similar_movie.id,
                        "title": similar_movie.title,
                        "year": similar_movie.release_date.split("-")[0],
                        "rating": similar_movie.vote_average,
                        "poster": f"{image_base_url}{image_size}/{similar_movie.poster_path}",
                    }
                )

        except:
            related_movies = []

        context = {
            "movie_id": movie.id,
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

        template = loader.get_template("pages/movie_page.html")
        return HttpResponse(template.render(context, request))


class TVView(View):
    def get(self, request, *args, **kwargs):
        config = Configuration().info()

        tmdb_tv = TV()
        content_id = kwargs["content_id"]
        tv = tmdb_tv.details(content_id)

        image_base_url = config.images.secure_base_url
        image_size = config.images.poster_sizes[1]

        watch_providers = []
        try:
            for provider in tmdb_tv.watch_providers(tv.id).results.IN.flatrate:
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

        cast = []

        for actor in tv.credits.cast:
            cast.append(
                {
                    "name": actor.name,
                    "id": actor.id,
                    "photo": f"{image_base_url}{image_size}/{actor.profile_path}",
                    "plays_character": actor.character,
                }
            )

        seasons = []
        try:
            for season in tv.seasons[1:]:
                seasons.append(
                    {
                        "id": season.id,
                        "name": season.name,
                        "year": season.air_date.split("-")[0],
                        "season_number": season.season_number,
                        "episode_count": season.episode_count,
                        "overview": season.overview,
                        "poster_path": f"{image_base_url}{image_size}/{season.poster_path}",
                    }
                )
        except:
            pass

        related_tv = []
        try:
            for similar_tv in tmdb_tv.similar(tv.id):
                related_tv.append(
                    {
                        "id": similar_tv.id,
                        "title": similar_tv.name,
                        "year": similar_tv.first_air_date.split("-")[0],
                        "rating": similar_tv.vote_average,
                        "poster": f"{image_base_url}{image_size}/{similar_tv.poster_path}",
                    }
                )
        except:
            related_tv = []

        director = {"name": "N/A", "id": None}
        writers = []
        for crew in tv.credits.crew:
            if crew["job"] == "Director":
                director["name"] = crew["name"]
                director["id"] = crew["id"]

            if crew["job"] == "Writer":
                writers.append({"name": crew["name"], "id": crew["id"]})

        context = {
            "tv_id": tv.id,
            "title": tv.name,
            "year": tv.first_air_date.split("-")[0],
            "release_date": tv.first_air_date,
            "poster": f"{image_base_url}{image_size}/{tv.poster_path}",
            "backdrop": f"{image_base_url}{image_size}/{tv.backdrop_path}",
            "overview": tv.overview,
            "genres": tv.genres,
            "rating": tv.vote_average,
            "rating_user_count": tv.vote_count,
            "seasons": seasons,
            "cast": cast,
            "director": director,
            "writers": writers,
            "stars": cast[0:4],
            "watch_providers": watch_providers,
            "related_tv": related_tv,
        }

        template = loader.get_template("pages/series_page.html")
        return HttpResponse(template.render(context, request))


class TVSeasonView(View):
    def get(self, request, *args, **kwargs):
        config = Configuration().info()

        tmdb_tv = TV()
        tmdb_season = Season()

        image_base_url = config.images.secure_base_url
        image_size = config.images.poster_sizes[1]

        tv_id = kwargs["tv_id"]
        season_number = kwargs["season_number"]
        series = tmdb_tv.details(tv_id)
        season = tmdb_season.details(tv_id=tv_id, season_num=season_number)

        cast = []

        for actor in season.credits.cast:
            cast.append(
                {
                    "name": actor.name,
                    "id": actor.id,
                    "photo": f"{image_base_url}{image_size}/{actor.profile_path}",
                    "plays_character": actor.character,
                }
            )

        watch_providers = []
        try:
            for provider in tmdb_tv.watch_providers(tv_id).results.IN.flatrate:
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

        director = {"name": "N/A", "id": None}
        writers = []
        for crew in season.credits.crew:
            if crew["job"] == "Director":
                director["name"] = crew["name"]
                director["id"] = crew["id"]

            if crew["job"] == "Writer":
                writers.append({"name": crew["name"], "id": crew["id"]})

        episodes = []

        for episode in season.episodes:
            episodes.append(
                {
                    "id": episode.id,
                    "number": episode.episode_number,
                    "name": episode.name,
                    "air_date": episode.air_date,
                    "overview": episode.overview,
                    "runtime": episode.runtime,
                    "rating": episode.vote_average,
                    "rating_user_count": episode.vote_count,
                    "poster": f"{image_base_url}{image_size}/{episode.still_path}",
                }
            )

        context = {
            "tv_id": tv_id,
            "season_id": season.id,
            "season_number": season.season_number,
            "title": f"{series.name} : {season.name}",
            "year": season.air_date.split("-")[0],
            "release_date": season.air_date,
            "poster": f"{image_base_url}{image_size}/{season.poster_path}",
            "overview": season.overview
            if season.overview != ""
            else "No description available",
            "cast": cast,
            "genres": series.genres,
            "director": director,
            "writers": writers,
            "stars": cast[0:4],
            "episodes": episodes,
            "watch_providers": watch_providers,
        }
        template = loader.get_template("pages/season_page.html")
        return HttpResponse(template.render(context, request))


class TVEpisodeView(View):
    def get(self, request, *args, **kwargs):
        config = Configuration().info()

        tmdb_tv = TV()
        tmdb_season = Season()
        tmdb_episode = Episode()

        image_base_url = config.images.secure_base_url
        image_size = config.images.poster_sizes[1]

        tv_id = kwargs["tv_id"]
        season_number = kwargs["season_number"]
        episode_number = kwargs["episode_number"]
        series = tmdb_tv.details(tv_id)
        season = tmdb_season.details(tv_id=tv_id, season_num=season_number)
        episode = tmdb_episode.details(
            tv_id=tv_id, season_num=season_number, episode_num=episode_number
        )

        cast = []

        for actor in season.credits.cast:
            cast.append(
                {
                    "name": actor.name,
                    "id": actor.id,
                    "photo": f"{image_base_url}{image_size}/{actor.profile_path}",
                    "plays_character": actor.character,
                }
            )

        for actor in episode.guest_stars:
            cast.append(
                {
                    "name": actor.name,
                    "id": actor.id,
                    "photo": f"{image_base_url}{image_size}/{actor.profile_path}",
                    "plays_character": actor.character,
                }
            )

        watch_providers = []
        try:
            for provider in tmdb_tv.watch_providers(tv_id).results.IN.flatrate:
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

        director = {"name": "N/A", "id": None}
        writers = []
        for crew in episode.crew:
            if crew["job"] == "Director":
                director["name"] = crew["name"]
                director["id"] = crew["id"]

            if crew["job"] == "Writer":
                writers.append({"name": crew["name"], "id": crew["id"]})

        context = {
            "tv_id": tv_id,
            "season_number": season_number,
            "episode_id": episode.id,
            "title": f"{episode.episode_number}: {episode.name}",
            "year": episode.air_date.split("-")[0],
            "release_date": episode.air_date,
            "poster": f"{image_base_url}{image_size}/{episode.still_path}",
            "overview": episode.overview
            if episode.overview != ""
            else "No description available",
            "cast": cast,
            "genres": series.genres,
            "director": director,
            "writers": writers,
            "stars": cast[0:4],
            "watch_providers": watch_providers,
        }
        template = loader.get_template("pages/episode_page.html")
        return HttpResponse(template.render(context, request))
