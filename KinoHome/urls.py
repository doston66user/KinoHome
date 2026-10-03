from django.urls import path
from .views import *


urlpatterns = [

    path('', main_page, name='main'),
    path('category/<int:pk>/', film_by_category_year, name='category'),
    path('year/<int:pk>/', film_by_year, name='year'),
    path('film/<int:pk>/', film_detail, name='film'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('about_us/', about_page, name='about_us'),
    path('registration/', register_user, name='register'),
    path('save_comment/<int:pk>', save_comment, name='save_comment'),
    path('comment_update/<int:pk>', CommentUpdate.as_view(), name='comment_update'),
    path('comment_delete/<int:pk>/<int:film_pk>/', delete_comment, name='comment_delete'),
    path('profile/', profile_view, name='profile'),
    path('edit/', edit_account_profile, name='edit'),
    # path('profile/delete-avatar/', delete_avatar, name='delete_avatar')
]

