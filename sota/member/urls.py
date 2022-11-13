from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login),
    path('loginCheck', views.loginCheck),
    path('logout', views.logout),
]


