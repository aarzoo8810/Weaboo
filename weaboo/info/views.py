from django.shortcuts import render
import requests
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from django.http import HttpResponse
import json

from .forms import AccountForm, LoginForm
from .mal_api import Mal
from .forms import BrowseAnimeForm


# Create your views here.
def index(request):
    # get list of current anime
    mal = Mal()
    season_list = mal.get_season(limit=11)["data"]
    popular_shows = mal.browse_anime(
        order_by="popularity", min_score=0.1)["data"]
    popular_manga_list = mal.get_top_manga(limit=10)
    print(request.user.is_authenticated)
    return render(request, "info/index.html", {"first_show": season_list[0],
                                               "shows": season_list[1:5],
                                               "seasonal_popular_shows": season_list[5:],
                                               "popular_shows": popular_shows[:6],
                                               "popular_manga": popular_manga_list,
                                               })


def search_view(request):
    mal = Mal()
    if request.GET:
        query = request.GET["q"]
        searched_shows = mal.browse_anime(q=query)["data"]
        return render(request, "info/browse_anime.html", {"shows": searched_shows})

    return HttpResponseRedirect(reverse("index"))


def popular_shows_view(request):
    mal = Mal()
    popular_shows = mal.browse_anime(
        order_by="popularity", min_score=0.1)["data"]
    return render(request, "info/browse_anime.html", {
        "shows": popular_shows,
    })


def anime_detail_view(request, mal_anime_id):
    mal = Mal()
    anime = mal.get_anime_details(mal_anime_id)
    recommendations = mal.get_anime_recommendation(mal_anime_id)
    if len(recommendations) > 0:
        return render(request, 'info/anime-details.html', {
            "show": anime,
            "recommendations": recommendations[:6],
        })
    else:
        return render(request, 'info/anime-details.html', {
            "show": anime
        })


def current_seasonal_anime(request):
    mal = Mal()
    endpoint = "https://api.jikan.moe/v4/seasons"
    response = requests.get(endpoint).json()["data"]

    season_list_dict = mal.get_season(filter="tv")
    season_list_item = season_list_dict["data"]
    season_list_page_count = season_list_dict["pagination"]["last_visible_page"]

    for page_num in range(2, season_list_page_count+1):
        print(page_num)
        season_list_item += mal.get_season(page=page_num, filter="tv")["data"]

    return render(request, "info/browse_anime.html", {
        "shows": season_list_item,
        "seasons": response
    })


def seasonal_anime(request, year, season):
    mal = Mal()
    endpoint = "https://api.jikan.moe/v4/seasons"
    response = requests.get(endpoint).json()["data"]

    season_list_dict = mal.get_season(filter="tv", year=year, season=season)
    season_list_item = season_list_dict["data"]
    season_list_page_count = season_list_dict["pagination"]["last_visible_page"]

    for page_num in range(2, season_list_page_count+1):
        season_list_item += mal.get_season(page=page_num, filter="tv")["data"]

    return render(request, "info/browse_anime.html", {
        "shows": season_list_item,
        "seasons": response
    })


def manga_details_view(request, mal_manga_id):
    mal = Mal()
    manga = mal.get_manga_details(mal_manga_id)
    recommendations = mal.get_manga_recommendation(mal_manga_id)

    if len(recommendations) > 0:
        return render(request, 'info/anime-details.html', {
            "show": manga,
            "type": "manga",
            "recommendations": recommendations[:6]
        })
    else:
        return render(request, 'info/anime-details.html', {
            "show": manga,
            "type": "manga"
        })


def browse_anime_view(request):
    mal = Mal()
    if request.GET:
        form = BrowseAnimeForm(request.GET)
        request.GET = request.GET.copy()
        for key in request.GET.keys():
            if not request.GET[key]:
                request.GET[key] = None
        # request.GET["limit"] = int(request.GET["limit"])
        # print(type(request.GET["limit"]))
        # limit = int(request.GET.pop("limit")[0])
        # print(type(limit))
        result = mal.browse_anime(**request.GET)["data"]
        print(len(result))
        return render(request, "info/browse_anime.html", {
            "shows": result,
            "form": form
        })
    form = BrowseAnimeForm()
    return render(request, "info/browse_anime.html", {
        "form": form
    })


def signup_view(request):
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(form.cleaned_data)
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
    else:
        form = AccountForm()

    return render(request, "info/signin.html", {
        "form": form
    })


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return HttpResponseRedirect(reverse("index"))
        
    else:
        form = AuthenticationForm()
    return render(request, 'info/signin.html', {'login_form': form})

