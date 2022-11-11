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
        try:
            user = User.objects.get(id=id,pw=pw)
        except:
            context = {
                'error' : '아이디 또는 비밀번호가 틀렸습니다.',
            }
            return render(request, 'login.html',context)
    if user is not None:
        request.session['login'] = user.idx
        return redirect('/')
    else:
        return render(request, 'login.html',context)

def certified(request:HttpRequest):
        try: 
            user = User.objects.get(idx= int(request.session['login']))
        except:
            return redirect('/member/login')
        if request.method =='POST':
            ppw  = request.POST.get('ppw')
        try:
            User.objects.get(idx=user.idx,ppw=ppw)
        except:
            context = {
                'error' : '공인인증번호가 틀렸습니다.',
            }
            return render(request, 'certified.html',context)

        if user is not None:
            request.session['ppw'] = user.idx
            return redirect('/')
        else:
            return render(request, '/service/lookup',context)
        




        # if user is not None:
        #     request.session['login'] = user.idx
        # return redirect('/')
        # else:
        #     return render(request, 'certified.html',context)