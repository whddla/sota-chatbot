from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def chatbot(request):
    return render(request,'chatbot.html')