from django.shortcuts import render, redirect
from sota.models import Deposit,DProduct,Card, CProduct, LProduct

def card(request):
    return render(request, 'product/card.html')

def deposit(request):
    dp = DProduct.objects.all()
    context = {
        'dp':dp
    }
    return render(request, 'product/deposit.html',context)

def loans(request):
    lp = LProduct.objects.all()
    list = []
    for i in lp:
        if i.user_idx is not None:
            pass
        else:
            list.append(i)
    context = {
        'p':list
    }
    return render(request, 'product/loans.html', context)