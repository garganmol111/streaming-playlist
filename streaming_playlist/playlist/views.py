import json
import random

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.forms import HiddenInput, ModelForm
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.list import ListView

from streaming_playlist.content import utils as content_utils

from .models import Playlist, PlaylistContent


class PlaylistBaseView(View):
    model = Playlist
    fields = ["name"]
    success_url = reverse_lazy("playlist:list_playlist")


class PlaylistCreateView(PlaylistBaseView, SuccessMessageMixin, CreateView):

    success_message = "Playlist created successfully!"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PlaylistCreateView, self).form_valid(form)


class PlaylistListView(PlaylistBaseView, ListView):
    """"""


class PlaylistDeleteView(PlaylistBaseView, SuccessMessageMixin, DeleteView):
    """"""

    success_message = "Playlist deleted successfully!"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(PlaylistDeleteView, self).delete(request, *args, **kwargs)


class PlaylistDetailView(View):
    def get(self, request, *args, **kwargs):

        shuffle = bool(request.GET.get("shuffle", "False"))
        playlist_id = kwargs["pk"]

        playlist = Playlist.objects.get(id=playlist_id)
        playlist_content = PlaylistContent.objects.filter(
            playlist__id=playlist_id
        ).select_related()

        extracted_content = []

        for content in playlist_content:
            if content.content_type == "movie":
                movie = content_utils.get_movie_info(content.content)

                redirect_url = reverse_lazy(
                    "content:get_movie",
                    kwargs={"content_id": movie["movie_id"]},
                )
                watch_providers = None
                if episode["watch_providers"] is not None:
                    watch_providers = [
                        i["provider_name"] for i in episode["watch_providers"]
                    ]
                extracted_content.append(
                    {
                        "type": "movie",
                        "playlist_content_id": content.id,
                        "redirect_url": redirect_url,
                        "id": movie["movie_id"],
                        "title": movie["title"],
                        "year": movie["year"],
                        "release_date": movie["release_date"],
                        "poster": movie["poster"],
                        "overview": movie["overview"],
                        "watch_providers": ",".join(watch_providers)
                        if watch_providers
                        else "Not available for streaming",
                    }
                )

            if content.content_type == "episode":
                episode = content_utils.get_episode_info(
                    content.series, content.season, content.episode_num
                )
                redirect_url = reverse_lazy(
                    "content:get_episode",
                    kwargs={
                        "tv_id": episode["tv_id"],
                        "season_number": episode["season_number"],
                        "episode_number": episode["episode_num"],
                    },
                )
                watch_providers = None
                if episode["watch_providers"] is not None:
                    watch_providers = [
                        i["provider_name"] for i in episode["watch_providers"]
                    ]

                extracted_content.append(
                    {
                        "type": "episode",
                        "playlist_content_id": content.id,
                        "redirect_url": redirect_url,
                        "title": f"{episode['title']} ({episode['tv_name']} - Season {episode['season_number']})",
                        "year": episode["year"],
                        "release_date": episode["release_date"],
                        "poster": episode["poster"],
                        "overview": episode["overview"],
                        "watch_providers": ",".join(watch_providers)
                        if watch_providers
                        else "Not available for streaming",
                    }
                )

        if shuffle:
            random.shuffle(extracted_content)
        context = {
            "playlist": playlist,
            "playlist_content": extracted_content,
        }
        template = loader.get_template("playlist/playlist_detail.html")
        return HttpResponse(template.render(context, request))


class PlaylistContentCreateForm(ModelForm):
    class Meta:
        model = PlaylistContent
        fields = "__all__"


class PlaylistContentCreateView(SuccessMessageMixin, CreateView):
    model = PlaylistContent
    template_name = "playlist/playlistcontent_form.html"
    form_class = PlaylistContentCreateForm

    def get(self, request, *args, **kwargs):

        if "type" not in request.GET and "id" not in request.GET:
            raise ValidationError("Invalid Request")

        if (
            request.GET["type"] == "episode"
            and "num" not in request.GET
            and "season" not in request.GET
            and "series" not in request.GET
        ):
            raise ValidationError("Invalid Request")

        initial = {
            "content_type": request.GET["type"],
            "content": request.GET["id"],
            "season": None,
            "series": None,
            "episode_num": None,
        }
        if request.GET["type"] == "episode":
            initial["season"] = request.GET["season"]
            initial["series"] = request.GET["series"]
            initial["episode_num"] = request.GET["num"]

        elif request.GET["type"] == "season":
            initial["season"] = request.GET["season"]
            initial["series"] = request.GET["series"]

        elif request.GET["type"] == "series":
            initial["series"] = request.GET["series"]

        form = self.form_class(initial=initial)

        form.fields["content"].widget = HiddenInput()
        form.fields["content_type"].widget = HiddenInput()
        form.fields["episode_num"].widget = HiddenInput()
        form.fields["series"].widget = HiddenInput()
        form.fields["season"].widget = HiddenInput()

        context = {"form": form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        already_exists = False
        playlist = Playlist.objects.filter(id=request.POST["playlist"]).first()

        for playlist_content in PlaylistContent.objects.filter(
            content=request.POST["content"]
        ):
            if str(playlist_content.playlist.id) == request.POST["playlist"]:
                already_exists = True

        self.success_url = "/" + "/".join(request.META["HTTP_REFERER"].split("/")[3:])

        if request.POST["content_type"] == "series":
            series = content_utils.get_tv_info(request.POST["series"])
            for season in series["seasons"]:

                season = content_utils.get_season_info(
                    request.POST["series"], season["season_number"]
                )

                for episode in season["episodes"]:

                    already_exists_episode = False
                    playlist = Playlist.objects.filter(
                        id=request.POST["playlist"]
                    ).first()

                    for playlist_content in PlaylistContent.objects.filter(
                        season=season["season_number"], episode_num=episode["number"]
                    ):
                        if (
                            str(playlist_content.playlist.id)
                            == request.POST["playlist"]
                        ):
                            already_exists_episode = True

                    if not already_exists_episode:
                        playlist_content = PlaylistContent(
                            playlist_id=request.POST["playlist"],
                            content=request.POST["content"],
                            content_type="episode",
                            season=season["season_number"],
                            series=request.POST["series"],
                            episode_num=episode["number"],
                        )

                        playlist_content.save()

            self.success_message = "Added series to playlist"

            messages.success(request, self.success_message)

        elif request.POST["content_type"] == "season":
            season = content_utils.get_season_info(
                request.POST["series"], request.POST["season"]
            )

            for episode in season["episodes"]:

                already_exists_episode = False
                playlist = Playlist.objects.filter(id=request.POST["playlist"]).first()

                for playlist_content in PlaylistContent.objects.filter(
                    episode_num=episode["number"]
                ):
                    if str(playlist_content.playlist.id) == request.POST["playlist"]:
                        already_exists_episode = True

                if not already_exists_episode:
                    playlist_content = PlaylistContent(
                        playlist_id=request.POST["playlist"],
                        content=request.POST["content"],
                        content_type="episode",
                        season=request.POST["season"],
                        series=request.POST["series"],
                        episode_num=episode["number"],
                    )

                    playlist_content.save()

            self.success_message = "Added season to playlist"

            messages.success(request, self.success_message)

        else:

            form = self.form_class(request.POST)

            if not already_exists:
                form.is_valid()
                instance = form.save(commit=False)
                instance.save()

            self.success_message = f"Added to playlist {playlist.name}"

            messages.success(request, self.success_message)

        return redirect("/" + "/".join(request.META["HTTP_REFERER"].split("/")[3:]))


class PlaylistContentDeleteView(SuccessMessageMixin, DeleteView):
    # success_url = reverse_lazy("playlist:get_playlist")
    model = PlaylistContent
    success_message = "Entry deleted successfully!"

    def delete(self, request, *args, **kwargs):
        playlist_content = PlaylistContent.objects.get(id=kwargs["pk"])
        self.success_url = reverse_lazy(
            "playlist:get_playlist", kwargs={"pk": playlist_content.playlist.id}
        )
        messages.success(self.request, self.success_message)
        return super(PlaylistContentDeleteView, self).delete(request, *args, **kwargs)
