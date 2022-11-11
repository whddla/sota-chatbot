from django.urls import path
from . import views


urlpatterns = [
    path('lookup/', views.lookup),
    path('looking',views.looking),
    path('send', views.send),
    path('loans/', views.loans),
    path('deposit/', views.deposit),
    path('loss/', views.loss),
    path('checkMoney', views.checkMoney),
    path('check', views.check),
    path('sendMoney', views.sendMoney),
    path('checkLoans', views.checkLoans),
    path('sendLoans', views.sendLoans),
    path('depositCheck', views.depositCheck),
    path('sendDeposit', views.sendDeposit),
]