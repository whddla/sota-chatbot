from django.shortcuts import render,redirect
from django.http import HttpRequest, JsonResponse, HttpResponse
from sota.models import User,Deposit,DProduct,Card, CProduct, LProduct,Transation
import simplejson as json

def lookup(request):
    try: 
        user = User.objects.get(idx= int(request.session['login']))
    except:
        return redirect('/member/login')
    user_idx = user.idx


    trans = Transation.objects.select_related('user_idx').filter(user_idx=user_idx).order_by('-date')
    pro = Card.objects.filter(user_idx=user_idx)
    cpro = CProduct.objects.all()

    # 내가 가진 입출금, 적금 총액
    total = 0
    for i in pro:
        total += i.remain

    loans = LProduct.objects.select_related('user_idx').filter(user_idx=user_idx) 
    deposit = Deposit.objects.select_related('user_idx').filter(user_idx=user_idx) 
    deposit_name = DProduct.objects.all()

    for i in deposit:
        total += i.remain
    l_remain = 0
    for i in loans:
        l_remain += i.remain


    context = {
        # 'card_name': card_name,
        'cpro':cpro,
        'pro': pro,
        'loans':loans,
        'dep':deposit,
        'dep_name':deposit_name,
        'l_remain':l_remain,
        'remain':total,
        'trans':trans,
    }

    return render(request, 'lookup.html',context)


def checkMoney(request:HttpRequest):
    try: 
        user = User.objects.get(idx= int(request.session['login']))
    except:
        return redirect('/member/login')
    if request.method == 'GET':
        ac = request.GET['account']
        my = Card.objects.get(user_idx=user.idx,account=ac)
    context = {
        'result' : my.remain
    }
    return HttpResponse(json.dumps(context), content_type="application/json")    



def send(request:HttpRequest):
    try: 
        user = User.objects.get(idx= int(request.session['login']))
    except:
        return redirect('/member/login')
    user_idx = user.idx
    if request.method =='POST':
        myNum = request.POST.get('my_num')
        mypw = request.POST.get('outPw')
        mysm = request.POST.get('myMoney')
        account = request.POST.get('num')
        print(myNum)
        print(mypw)
        print(mysm)
        print(account)
        if Card.objects.get(user_idx=user_idx,account=account,card_pw=mypw) ==None:

            c_pro = CProduct.objects.all()
        
    context = {
        'card':card,
        'c_pro':c_pro,

    }

    return render(request, 'send.html',context)



def loans(request):
    return render(request, 'loans.html')
def deposit(request):
    return render(request, 'deposit.html')
def loss(request):
    return render(request, 'loss.html')