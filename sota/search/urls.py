from django.urls import path
from . import views

urlpatterns = [
    path('card/', views.card),
    path('cardApply/', views.cardApply),
    path('deposit/', views.deposit),
    path('loans/', views.loans),
]