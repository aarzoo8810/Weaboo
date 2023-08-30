from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("anime/<int:mal_anime_id>", views.anime_detail_view, name='anime-details'),
    path("manga/<int:mal_manga_id>", views.manga_details_view, name='manga-details'),
    path("browse/anime", views.browse_anime_view, name="browse-anime")
]

