from django.contrib.auth import get_user_model
from django.urls import reverse
from django.views import View
from django.http import HttpResponse

from tmdbv3api import Movie, TV, Episode
import json


class SearchView(View):
    def get(self, request, *args, **kwargs):
        pass
