from django.shortcuts import render, redirect
# from ddm.models import Member

def card(request):
    return render(request, 'card.html')
def deposit(request):
    return render(request, 'deposit.html')
def loans(request):
    return render(request, 'loans.html')