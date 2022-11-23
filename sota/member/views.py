from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse, HttpResponse
from sota.models import User

    
def login(request):
    return render(request, 'login.html')

def logout(request):
    if request.session['login'] is not None:
        request.session['login'] = None
        return redirect('/')
    return render(request, 'login.html')

def loginCheck(request:HttpRequest):
    if request.method =='POST':
        id = request.POST.get('id')
        pw = request.POST.get('pw')
        ppw = request.POST.get('ppw')
        try:
            user = User.objects.get(id=id,pw=pw,p_pw=ppw)
        except:
            context = {
                'error' : '입력된 정보가 틀렸습니다.',
            }
            return render(request, 'login.html',context)
    if user is not None:
        request.session['login'] = user.idx
        return redirect('/')
    else:
        return render(request, 'login.html',context)

        