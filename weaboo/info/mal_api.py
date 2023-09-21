import requests


class Mal:

    def get_anime_details(self, mal_anime_id):
        """Get anime info by mal_id else return status code"""
        print(mal_anime_id)
        endpoint = f"https://api.jikan.moe/v4/anime/{mal_anime_id}/full"
        response = requests.get(endpoint)

        try:
            print(response.json())
            response_json = response.json()["data"]
        except TypeError:
            return response.status_code
        else:
            return response_json

    def get_anime_recommendation(self, mal_anime_id):
        endpoint = f"https://api.jikan.moe/v4/anime/{mal_anime_id}/recommendations"
        response = requests.get(endpoint)
        response_json = response.json()["data"]

        return response_json

    def get_manga_details(self, mal_manga_id):
        """Get anime info by mal_id else return status code"""
        endpoint = f"https://api.jikan.moe/v4/manga/{mal_manga_id}/full"
        response = requests.get(endpoint)

        try:
            response_json = response.json()["data"]
        except TypeError:
            return response.status_code
        else:
            return response_json

    def get_manga_recommendation(self, mal_manga_id):
        endpoint = f"https://api.jikan.moe/v4/manga/{mal_manga_id}/recommendations"
        response = requests.get(endpoint)
        response_json = response.json()["data"]

        return response_json

    def get_season(self, year: int = None, season: str = None, filter: str = None, sfw: bool = True, limit: str = None, page: int = 1) -> dict:
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

    def get_top_manga(self, type: str = "manga", filter: str = "bypopularity", page: int = 1, limit: int = None):
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


    def get_top_anime(self, type: str=None, filter: str=None, rating: str=None, page: int=1, limit: int=None):
        endpoint = "https://api.jikan.moe/v4/top/anime"
        params = {
            "type": type,
            "filter": filter,
            "page": page,
            "limit": limit
        }
        response = requests.get(endpoint, params=params)
        print(response.status_code)
        response_json = response.json()
        return response_json

    def browse_anime(self,
                     sfw: bool = False,
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
                     end_date: str = None
                     ):
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
