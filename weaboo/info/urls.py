from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("search", views.search_view, name="search"),
    path("anime/<int:mal_anime_id>", views.anime_detail_view, name='anime-details'),
    path("anime/add/<int:mal_anime_id>/<int:list_id>", views.add_anime, name='add-anime'),
    path("anime/popular", views.popular_shows_view, name="popular"),
    path("anime/seasonal", views.current_seasonal_anime, name="current-seasonal-anime"),
    path("anime/seasonal/<int:year>/<str:season>", views.seasonal_anime, name="seasonal-anime"),
    path("manga/<int:mal_manga_id>", views.manga_details_view, name='manga-details'),
    path("browse/anime", views.browse_anime_view, name="browse-anime"),
    path("signup", views.signup_view, name="signup"),
    path("login", views.login_view, name="login"),
    path("anime/list/<int:user_id>/", views.user_list_view, name="user-list"),
    path("logout", views.logout_view, name="logout"),
]

