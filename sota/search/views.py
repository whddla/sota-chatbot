from django.shortcuts import render, redirect
# from ddm.models import Member

def card(request):
    return render(request, 'product/card.html')
def deposit(request):
    return render(request, 'product/deposit.html')
def loans(request):
    return render(request, 'product/loans.html')