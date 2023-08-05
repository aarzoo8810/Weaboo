from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("anime/<int:mal_anime_id>", views.anime_info),
    path("manga/<int:mal_manga_id>", views.manga_info),
]

