from django.urls import path
from . import views


urlpatterns = [
    path('lookup/', views.lookup),
    path('looking',views.looking),
    path('loans_detail',views.loans_detail),
    path('send', views.send),
    path('loans/', views.loans),
    path('deposit/', views.deposit),
    path('loss/', views.loss),
    path('loss_detail/', views.loss_detail),
    path('loss_suc/', views.loss_suc),
    path('checkMoney', views.checkMoney),
    path('check', views.check),
    path('sendMoney', views.sendMoney),
    path('checkLoans', views.checkLoans),
    path('sendLoans', views.sendLoans),
    path('depositCheck', views.depositCheck),
    path('sendDeposit', views.sendDeposit),
]