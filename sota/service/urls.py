from django.urls import path
from . import views


urlpatterns = [
    path('lookup/', views.lookup),
    path('send/', views.send),
    path('loans/', views.loans),
    path('deposit/', views.deposit),
]