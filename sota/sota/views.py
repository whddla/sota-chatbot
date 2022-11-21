from django.shortcuts import render,redirect
from sota.models import User,LProduct,Deposit,Card,Transation
def index(request):
    try: 
        user = User.objects.get(idx= int(request.session['login']))
    except:
        return redirect('/member/login')
    lp = LProduct.objects.filter(user_idx=user.idx)
    dp = Deposit.objects.filter(user_idx=user.idx)
    c = Card.objects.filter(user_idx=user.idx)
    trans = []
    for i in lp:
        ac = i.account
        trans.append(Transation.objects.filter(user_idx=user.idx, account=ac).last())
    context = {
        'user':user,
        'lp':lp,
        'dp':dp,
        'c':c,
        'trans':trans
    }
    return render(request, 'index.html',context)