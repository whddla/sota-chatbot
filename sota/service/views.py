from django.shortcuts import render

# Create your views here.
def lookup(request):
    return render(request, 'lookup.html')
def send(request):
    return render(request, 'send.html')
def loans(request):
    return render(request, 'loans.html')