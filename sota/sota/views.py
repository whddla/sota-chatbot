from django.shortcuts import render,redirect
from sota.models import User,Deposit,DProduct,Card, CProduct, LProduct,Transation
def index(request):
    try: 
        user = User.objects.get(idx= int(request.session['login']))
    except:
        return redirect('/member/login')
    context = {
        'user':user,
    }
    return render(request, 'index.html',context)
