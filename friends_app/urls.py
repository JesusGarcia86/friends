from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_reroute),
    path('main', views.login),
    path('create_user', views.register),
    path('log_in', views.log_in),
    path('logout', views.logout),
    path('friends', views.friends),
    path('add', views.add),
    path('profile/<int:user_id>', views.profile),
]