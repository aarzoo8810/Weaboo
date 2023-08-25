from django.shortcuts import render

# Create your views here.


from django.shortcuts import render
import requests
from django.http import HttpResponse


# Create your views here.
def index(request):
    # get list of current anime
    season_list = get_season(limit=11)
    popular_manga_list = get_top_manga(limit=10)
    return render(request, "info/index.html", {"first_show": season_list[0],
                                               "shows": season_list[1:5],
                                               "popular_shows": season_list[5:],
                                               "popular_manga": popular_manga_list,
                                               })


def anime_info(request, mal_anime_id):
    """Get anime info by mal_id"""
    endpoint = f"https://api.jikan.moe/v4/anime/{mal_anime_id}/full"
    response = requests.get(endpoint)
    response_json = response.json()["data"]
    recommendations = get_anime_recommendation(mal_anime_id)

    if len(recommendations) > 0:
        return render(request, 'info/anime-details.html', {
            "show": response_json,
            "recommendations": recommendations[:6],
        })
    else:
        return render(request, 'info/anime-details.html', {
            "show": response_json
        })


def manga_info(request, mal_manga_id):
    """Get anime info by mal_id"""
    endpoint = f"https://api.jikan.moe/v4/manga/{mal_manga_id}/full"
    response = requests.get(endpoint)
    response_json = response.json()["data"]
    recommendations = get_manga_recommendation(mal_manga_id)

    if len(recommendations) > 0:
        return render(request, 'info/anime-details.html', {
            "show": response_json,
            "type": "manga",
            "recommendations": recommendations[:6]
        })
    else:
        return render(request, 'info/anime-details.html', {
            "show": response_json,
            "type": "manga"
        })

def get_manga_recommendation(mal_manga_id):
    endpoint = f"https://api.jikan.moe/v4/manga/{mal_manga_id}/recommendations"
    response = requests.get(endpoint)
    response_json = response.json()["data"]

    return response_json



def get_season(year: int = None, season: str = None, filter: str = None, sfw: bool = False, limit: str = None, page: int = 1) -> dict:
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
    response_json = response.json()["data"]
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