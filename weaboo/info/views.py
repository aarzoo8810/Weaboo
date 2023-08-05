from django.shortcuts import render

# Create your views here.


from django.shortcuts import render
import requests


# Create your views here.




# def get_season(year: int = None, season: str = None, filter: str = None, sfw: bool = False, limit: str = None, page: int = 1):

#     endpoint = "https://api.jikan.moe/v4/seasons/"
#     if year and season:
#         endpoint += f"{year}/{season}"
#     else:
#         endpoint += "now"
         
#     if sfw:
#         endpoint += "?sfw"
#     params = {
#         "filter": filter,
#         "limit": limit,
#         "page": page,
#     }
#     response = requests.get(endpoint, params=params)
#     print(response.url)
#     print(response.status_code)
#     response_json = response.json()


# get_season(year=2023, season="summer", limit=5)
