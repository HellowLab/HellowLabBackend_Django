

from django.urls import path, include, re_path
from rest_framework.authtoken.views import obtain_auth_token
from .views import *

urlpatterns = [
    # update movie result
    path('movieresult/', MovieResultView.as_view(), name='movie_result'),
    path('singlemovieresult/', SingleMovieView.as_view(), name='single_movie_result'),
    path('tmdbindex/', TmdbIndexView.as_view(), name='tmdb_index')
]
