from django.urls import path

from .views import *

urlpatterns = [
    path('roles/', RolesView.as_view(), name='roles'),
]
