from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse, HttpResponse
# from ddm.models import Member

def login(request):
    return render(request, 'login.html')