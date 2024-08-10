

from django.urls import path, include, re_path
from rest_framework.authtoken.views import obtain_auth_token
from .views import *

urlpatterns = [
    # update movie result
    path('movieresult/', MovieResultView.as_view(), name='movie_result'),
    # path('update_user_data/', update_user_data, name='update_user_data'),
    # path('myuser', get_my_user, name='get_my_user'),

    # path('alltags/', tag_list, name='all-tagslist'),
    # path('tagitems/<int:item_id>/', ItemDetailView.as_view(), name='item-detail'),
    # path('tagitems/csvupload/', import_csv, name='tag_item_upload_csv'),

    # path('newcomment/', create_comment, name='create_comment'),
    # path('getcomments/<int:tagID>/', get_comment, name="get_comment_for_tag"),
]
