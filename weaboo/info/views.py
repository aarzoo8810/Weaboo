from django.shortcuts import render

# Create your views here.


from django.shortcuts import render
import requests
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import BrowseAnimeForm


# Create your views here.
def index(request):
    # get list of current anime
    season_list = get_season(limit=11)["data"]
    popular_shows = browse_anime(order_by="popularity", min_score=0.1)["data"]
    popular_manga_list = get_top_manga(limit=10)
    return render(request, "info/index.html", {"first_show": season_list[0],
                                               "shows": season_list[1:5],
                                               "seasonal_popular_shows": season_list[5:],
                                               "popular_shows": popular_shows[:6],
                                               "popular_manga": popular_manga_list,
                                               })


def search_view(request):
    if request.GET:
        query = request.GET["q"]
        searched_shows = browse_anime(q=query)["data"]
        return render(request, "info/browse_anime.html", {"shows": searched_shows})
    
    return HttpResponseRedirect(reverse("index"))


def popular_shows_view(request):
    popular_shows = browse_anime(order_by="popularity", min_score=0.1)["data"]
    return render(request, "info/browse_anime.html", {
        "shows": popular_shows,
    })


def anime_detail_view(request, mal_anime_id):

    anime = get_anime_details(mal_anime_id)
    recommendations = get_anime_recommendation(mal_anime_id)
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

    endpoint = "https://api.jikan.moe/v4/seasons"
    response = requests.get(endpoint).json()["data"]

    season_list_dict = get_season(filter="tv")
    season_list_item = season_list_dict["data"]
    season_list_page_count = season_list_dict["pagination"]["last_visible_page"]

    for page_num in range(2, season_list_page_count+1):
        print(page_num)
        season_list_item += get_season(page=page_num, filter="tv")["data"]

    return render(request, "info/browse_anime.html", {
        "shows": season_list_item,
        "seasons": response
    })


def seasonal_anime(request, year, season):
    endpoint = "https://api.jikan.moe/v4/seasons"
    response = requests.get(endpoint).json()["data"]

    season_list_dict = get_season(filter="tv", year=year, season=season)
    season_list_item = season_list_dict["data"]
    season_list_page_count = season_list_dict["pagination"]["last_visible_page"]

    for page_num in range(2, season_list_page_count+1):
        season_list_item += get_season(page=page_num, filter="tv")["data"]

    return render(request, "info/browse_anime.html", {
        "shows": season_list_item,
        "seasons": response
    })


def manga_details_view(request, mal_manga_id):

    manga = get_manga_details(mal_manga_id)
    recommendations = get_manga_recommendation(mal_manga_id)

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
        result = browse_anime(**request.GET)
        print(len(result))
        return render(request, "info/browse_anime.html", {
            "shows": result,
            "form": form
        })
    form = BrowseAnimeForm()
    return render(request, "info/browse_anime.html", {
        "form": form
    })


def get_anime_details(mal_anime_id):
    """Get anime info by mal_id else return status code"""
    endpoint = f"https://api.jikan.moe/v4/anime/{mal_anime_id}/full"
    response = requests.get(endpoint)

    try:
        response_json = response.json()["data"]
    except TypeError:
        return response.status_code
    else:
        return response_json


def get_manga_details(mal_manga_id):
    """Get anime info by mal_id else return status code"""
    endpoint = f"https://api.jikan.moe/v4/manga/{mal_manga_id}/full"
    response = requests.get(endpoint)

    try:
        response_json = response.json()["data"]
    except TypeError:
        return response.status_code
    else:
        return response_json


def get_manga_recommendation(mal_manga_id):
    endpoint = f"https://api.jikan.moe/v4/manga/{mal_manga_id}/recommendations"
    response = requests.get(endpoint)
    response_json = response.json()["data"]

    return response_json


def get_season(year: int = None, season: str = None, filter: str = None, sfw: bool = True, limit: str = None, page: int = 1) -> dict:
    """This function return a list of shows categorized as season in json.To get current season don't pass year and season parameter. Example 
    get_season(year=2015, season = 'fall', filter='movie', sfw=False, page=1, limit=10),

    get_season(year=2015, season = 'summer', filter='ova', sfw=False, page=5, limit=20)"""

    endpoint = "https://api.jikan.moe/v4/seasons/"
    if year and season:
        endpoint += f"{year}/{season}"
    else:
        endpoint += "now"

    if sfw:
        endpoint += "?sfw"
    params = {
        "filter": filter,
        "limit": limit,
        "page": page,
    }
    response = requests.get(endpoint, params=params)
    response_json = response.json()
    return response_json


def get_top_manga(type: str = "manga", filter: str = "bypopularity", page: int = 1, limit: int = None):
    """
    Get top manga. its by popularity by default
    type: 	 string (manga_search_query_type) 
             Enum: "manga" "novel" "lightnovel" "oneshot" "doujin" "manhwa" "manhua"
             Available Manga types

    filter:	string (top_manga_filter)
            Enum: "publishing" "upcoming" "bypopularity" "favorite"

            Top items filter types

    page: Integer

    limit: Integer
    """
    endpoint = "https://api.jikan.moe/v4/top/manga/"

    params = {
        "type": type,
        "filter": filter,
        "page": page,
        "limit": limit
    }
    response = requests.get(endpoint, params=params)
    print(response.status_code)
    response_json = response.json()
    return response_json["data"]


# get_season(year=2023, season="summer", limit=5)


def get_anime_recommendation(mal_anime_id):
    endpoint = f"https://api.jikan.moe/v4/anime/{mal_anime_id}/recommendations"
    response = requests.get(endpoint)
    response_json = response.json()["data"]

    return response_json


def browse_anime(sfw: bool = False,
                 page: int = 1,
                 limit: int = None,
                 q: str = None,
                 type: str = None,
                 score: float = None,
                 min_score: float = None,
                 max_score: float = None,
                 status: str = None,
                 rating: str = None,
                 genres: str = None,
                 genres_exclude: str = None,
                 order_by: str = None,
                 sort: str = None,
                 start_date: str = None,
                 end_date: str = None):
    """This Function returns a list of anime based on received parameters"""
    endpoint = "https://api.jikan.moe/v4/anime"

    if sfw:
        endpoint += "?sfw"

    params = {
        "page": page,
        "limit": limit,
        "q": q,
        "type": type,
        "score": score,
        "min_score": min_score,
        "max_score": max_score,
        "status": status,
        "rating": rating,
        "genres": genres,
        "genres_exclude": genres_exclude,
        "order_by": order_by,
        "sort": sort,
        "start_date": start_date,
        "end_date": end_date,
    }
    response = requests.get(endpoint, params=params)

    return response.json()
