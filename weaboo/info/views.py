from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
import json

import threading
import requests

from .forms import AccountForm, LoginForm
from .mal_api import Mal
from .forms import BrowseAnimeForm
from .models import CustomUser, ListType, UserShowList
import time


# Create your views here.
def index(request):
    # get list of current anime
    mal = Mal()
    season_list = mal.get_season(limit=11)["data"]
    popular_shows = mal.browse_anime(
        order_by="popularity", min_score=0.1)["data"]  # min_score=0.1 because a show with score 0 can be at the  top of the list which is wrong
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


def popular_manga_views(request):
    mal = Mal()
    popular_manga_list = mal.get_top_manga()

    return render(request, "info/browse_anime.html", {"shows": popular_manga_list,
                                                      "is_popular_manga": True,
                                                      "is_manga": True
                                                      })


def top_manga_views(request):
    mal = Mal()
    # by default filter="bypopularity" but we want top list
    top_manga_list = mal.get_top_manga(filter=None, type=None)
    top_manga_list = sorted(top_manga_list, key=lambda x: x["rank"])

    return render(request, "info/browse_anime.html", {"shows": top_manga_list,
                                                      "is_top_manga": True,
                                                      "is_manga": True
                                                      })


def top_shows_view(request):
    mal = Mal()
    top_shows = mal.get_top_anime()["data"]

    # sorting top_shows by rank because they are sorted by rating by default so
    # some shows which has higher rank can be below some shows with lowe rank
    # because of equal rating
    # also reverse = True if needed
    top_shows = sorted(top_shows, key=lambda x: x["rank"])
    return render(request, "info/browse_anime.html", {"shows": top_shows,
                                                      "is_top": True})


def anime_detail_view(request, mal_anime_id):
    mal = Mal()
    anime = mal.get_anime_details(mal_anime_id)
    list_types = ListType.objects.all()
    user = request.user

    recommendations = mal.get_anime_recommendation(mal_anime_id)
    if len(recommendations) == 0:
        recommendations = None
    else:
        recommendations = recommendations[:6]

    try:
        user_list_status = UserShowList.objects.get(
            user=user, mal_id=mal_anime_id).list.get()
    except ObjectDoesNotExist:
        user_list_status = None

    return render(request, 'info/anime-details.html', {
        "show": anime,
        "recommendations": recommendations,
        "list_types": list_types,
        "user_list_status": user_list_status
    })


def add_anime(request, mal_anime_id, list_id):
    """Function for adding a show to user's list"""
    if request.user.is_authenticated:
        user_id = request.user.id
        print(mal_anime_id, list_id, user_id)

        # check if show already exists for user if it does update it
        user = CustomUser.objects.filter(id=user_id)
        list = ListType.objects.filter(id=list_id)

        try:
            user_show_list = user[0].user_show_list.get(mal_id=mal_anime_id)
        except ObjectDoesNotExist:
            user_show_list_instance = UserShowList.objects.create(
                mal_id=mal_anime_id)
            user_show_list_instance.user.set(user)
            user_show_list_instance.list.set(list)
        else:
            user_show_list.list.set(list)

        return redirect("anime-details", mal_anime_id=mal_anime_id)
    else:
        return HttpResponseRedirect(reverse("login"))


def delete_anime(request, mal_anime_id):
    UserShowList.objects.get(user=request.user, mal_id=mal_anime_id).delete()
    return redirect("user-list", user_id=request.user.id)


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
    endpoint = "https://api.jikan.moe/v4/seasons"
    response = requests.get(endpoint).json()["data"]
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
            "form": form,
            "seasons": response,
        })
    form = BrowseAnimeForm()
    return render(request, "info/browse_anime.html", {
        "form": form,
        "seasons": response
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


def user_list_view(request, user_id):

    if request.method == "POST":
        mal_id = int(request.POST["hidden-mal-id"])
        total_episodes = int(request.POST["total-episodes"])
        episode_num = int(request.POST["episode-number"])
        watching_status_id = int(request.POST["watching-status"])

        # get list object from database to save in UserListShow
        list_type = ListType.objects.filter(id=watching_status_id)

        user_show_list = UserShowList.objects.get(mal_id=mal_id)
        user_show_list.list.set(list_type)

        # id=3 is a for completed show
        # if it is true we are going to set episode_watched = total_episodes
        if list_type[0].id == 3 and user_show_list.episode_watched != episode_num:
            user_show_list.episode_watched = episode_num
        elif list_type[0].id == 3:
            user_show_list.episode_watched = total_episodes
        user_show_list.save()

        user = CustomUser.objects.get(id=user_id)
        user_list = user.user_show_list.all().order_by("-id")
        status_list = ListType.objects.all()
        shows = user_list_helper_func(user_list)

        return render(request, "info/user_list.html", {"user": user,
                                                       "shows": shows,
                                                       "user_list": user_list,
                                                       "status_list": status_list})

    else:
        user = CustomUser.objects.get(id=user_id)
        user_list = user.user_show_list.all().order_by("-id")
        status_list = ListType.objects.all()
        shows = user_list_helper_func(user_list)

    return render(request, "info/user_list.html", {"user": user,
                                                   "shows": shows,
                                                   "user_list": user_list,
                                                   "status_list": status_list})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))



def user_list_helper_func(user_list):
    start = time.time()
    mal = Mal()
    shows = []
    threads = [threading.Thread(target=lambda item=item: shows.append(mal.get_anime_details(item.mal_id, {
                                    "watching_status": item.list.get(), "episodes_watched": item.episode_watched}))) for item in user_list]
    time_interval = 2.3 / 3  # 3 is maximum number of threads executed per second
    print(time_interval)
    for thread in threads:
        thread.start()
        time.sleep(time_interval)
    for thread in threads:
        thread.join()

    end = time.time()
    print(end - start)
    return shows