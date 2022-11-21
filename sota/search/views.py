from django.shortcuts import render, redirect
from sota.models import Deposit,DProduct,Card, CProduct, LProduct,User

# 카드 상품
def card(request):
    user = User.objects.get(idx= int(request.session['login']))
    cp = CProduct.objects.all()
    context = {
        'user':user,
        'cpro':cp
    }
    return render(request, 'product/card.html',context)

# 카드 신청
def cardApply(request):
    user = User.objects.get(idx= int(request.session['login']))
    idx = request.GET.get('idx')
    cpro = CProduct.objects.get(idx=idx)
    
    context = {
        'user':user,
        'cpro': cpro
    }
    return render(request, 'product/cardApply.html',context)

# 적금 상품
def deposit(request):
    user = User.objects.get(idx= int(request.session['login']))
    dp = DProduct.objects.all()
    context = {
        'user':user,
        'dp':dp
    }
    return render(request, 'product/deposit.html',context)

# 대출 상품
def loans(request):
    user = User.objects.get(idx= int(request.session['login']))
    lp = LProduct.objects.all()
    lpCnt = LProduct.objects.filter(user_idx=None)
    list = []
    for i in lp:
        if i.user_idx is not None:
            pass
        else:
            list.append(i)
    context = {
        'lp':lp,
        'lpCnt':lpCnt,
        'user':user,
        'p':list
    }
    return render(request, 'product/loans.html', context)