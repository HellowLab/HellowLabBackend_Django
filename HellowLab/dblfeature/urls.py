

from django.urls import path, include, re_path
from rest_framework.authtoken.views import obtain_auth_token
from .views import *

urlpatterns = [
    # update movie result
    path('movieresult/', MovieResultView.as_view(), name='movie_result'),
    path('singlemovieresult/', SingleMovieView.as_view(), name='single_movie_result'),
    path('tmdbindex/', TmdbIndexView.as_view(), name='tmdb_index'),
    path('movielists/', MovieListView.as_view(), name='movie_list'),
    path('movielists/<int:list_id>/', MovieListView.as_view(), name='movie_list_detail'),
    path('movielists/<int:list_id>/items/', MovieListItemView.as_view(), name='movie_list_item'),
    path('movielists/<int:list_id>/items/<str:item_id>/', MovieListItemView.as_view(), name='movie_list_item_detail'),
]
