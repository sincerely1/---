from django.urls import path

from .views import *

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('getinfo/',UserInfoView.as_view(),name='userinfo'),
    path('logout/',UserLogoutView.as_view(),name='logout'),
    path('getusers/',GetUsersView.as_view(),name='get_users'),
    path('adduser/',AddUserView.as_view(),name='add_user'),
    path('deluser/',DelUserView.as_view(),name='del_user'),
    path('update_userinfo/',UpdateUserinfo.as_view(),name='update_user_info'),
    path('updateuser/',UpdateUser.as_view(),name='update_user'),

]
