from django.contrib.auth import get_user_model
from django.urls import reverse
from django.views import View
from django.http import HttpResponse
from django.template import loader


from tmdbv3api import Search, Configuration
import json


class SearchView(View):
    def get(self, request, *args, **kwargs):

        title = request.GET["title"]
        config = Configuration().info()
        image_base_url = config.images.secure_base_url
        image_size = config.images.poster_sizes[1]

        tmdb_search = Search()
        movies = tmdb_search.movies({"query": title})
        series = tmdb_search.tv_shows({"query": title})

        movie_results = []

        for movie in movies:
            movie_results.append(
                {
                    "type": "movie",
                    "title": movie.title,
                    "id": movie.id,
                    "year": movie.release_date.split("-")[0],
                    "overview": movie.overview,
                    "rating": movie.vote_average,
                    "rating_votes_count": movie.vote_count,
                    "poster": f"{image_base_url}{image_size}/{movie.poster_path}",
                    "redirect_url": reverse(
                        "content:get_movie", kwargs={"content_id": movie.id}
                    ),
                }
            )

        tv_results = []
        for serie in series:
            tv_results.append(
                {
                    "type": "series",
                    "title": serie.name,
                    "id": serie.id,
                    "year": serie.first_air_date.split("-")[0],
                    "overview": serie.overview,
                    "rating": serie.vote_average,
                    "rating_votes_count": serie.vote_count,
                    "poster": f"{image_base_url}{image_size}/{serie.poster_path}",
                    "redirect_url": reverse(
                        "content:get_tv", kwargs={"content_id": serie.id}
                    ),
                }
            )

        context = {
            "query": title,
            "total_results": len(movie_results) + len(tv_results),
            "movie_results": len(movie_results),
            "tv_results": len(tv_results),
            "movies": movie_results,
            "tvs": tv_results,
        }

        template = loader.get_template("pages/search_page.html")
        return HttpResponse(template.render(context, request))
