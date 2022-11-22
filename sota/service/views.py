from django.shortcuts import render,redirect
from django.http import HttpRequest, JsonResponse, HttpResponse
from sota.models import User,Deposit,DProduct,Card, CProduct, LProduct,Transation
import simplejson as json
import datetime as dt



def lookup(request:HttpRequest):
    try: 
        user = User.objects.get(idx= int(request.session['login']))
    except:
        return redirect('/member/login')
    user_idx = user.idx

    trans = Transation.objects.select_related('user_idx').filter(user_idx=user_idx).order_by('-date')
    card = Card.objects.filter(user_idx=user_idx)
    cpro = CProduct.objects.all()

    # 내가 가진 입출금, 적금 총액
    total = 0
    for i in card:
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
        'user':user,
        'cpro':cpro,
        'pro': card,
        'loans':loans,
        'dep':deposit,
        'dep_name':deposit_name,
        'l_remain':l_remain,
        'remain':total,
        'trans':trans,
    }

    return render(request, 'lookup.html',context)




def looking(request):
    try: 
        user = User.objects.get(idx= int(request.session['login']))
    except:
        return redirect('/member/login')
    ac = request.GET.get('account')
    trans = Transation.objects.filter(account=ac).all()
    
    for i in trans:
        remain = i

    context={
        'trans':trans,
        'user':user,
        'remain':remain
    }

    return render(request, 'looking.html',context)


def filter(request:HttpRequest):
    try: 
        user = User.objects.get(idx= int(request.session['login']))
    except:
        return redirect('/member/login')
    if request.method=='GET':
        ac = request.GET.get('account')
        print(ac)
        # 필터를 적용했을때 거래내역
        # 입금/출금
        inp = request.GET.get('inp')
        # 시작일
        sday = request.GET.get('startday')
        # 마지막일
        lday = request.GET.get('lastday')

        # 입/출금이 없다면
        if inp=='' and sday == '' and lday =='':
            trans = Transation.objects.filter(account=ac)
            try:
                Card.objects.filter(account=ac)
            except:
                remain = Deposit.objects.get(account=ac)
                context={
                    'trans':trans,
                    'user':user,
                    'remain':remain
                }

                return render(request, 'looking.html',context)
            else:
                remain = Card.objects.get(account=ac)
                print(remain)
                context={
                    'trans':trans,
                    'user':user,
                    'remain':remain
                }
                return render(request, 'looking.html',context)
        elif inp == '':
            sday = request.GET.get('startday') 
            # 마지막일
            lday = request.GET.get('lastday') 
            trans = Transation.objects.filter(account=ac,date__range=[sday, lday])
            # 예금계좌라면
            try:
                remain = Card.objects.get(account=ac)
            # 예금이 아니면 적금계좌
            except:
                remain = Deposit.objects.get(deposit_num=ac)
                context={
                    'trans':trans,
                    'user':user,
                    'remain':remain
                }
                return render(request, 'looking.html',context)
            else:
                remain = Card.objects.get(account=ac)
                print(remain)
                context={
                    'trans':trans,
                    'user':user,
                    'remain':remain
                }
                return render(request, 'looking.html',context)
        elif sday == '' or lday =='':
            trans = Transation.objects.filter(account=ac,kind=int(inp))
            try:
                Card.objects.filter(account=ac)
            except:
                remain = Deposit.objects.get(account=ac)
                context={
                    'trans':trans,
                    'user':user,
                    'remain':remain
                }

                return render(request, 'looking.html',context)
            else:
                remain = Card.objects.get(account=ac)
                context={
                    'trans':trans,
                    'user':user,
                    'remain':remain
                }

                return render(request, 'looking.html',context)
        else:
            trans = Transation.objects.filter(account=ac,kind=int(inp),date__range=[sday, lday])

            try:
                Card.objects.filter(account=ac)
            except:
                remain = Deposit.objects.get(account=ac)
                context={
                    'trans':trans,
                    'user':user,
                    'remain':remain
                }

                return render(request, 'looking.html',context)
            else:
                remain = Card.objects.get(account=ac)
                context={
                    'trans':trans,
                    'user':user,
                    'remain':remain
                }

                return render(request, 'looking.html',context)

def loans_detail(request):
    try: 
        user = User.objects.get(idx= int(request.session['login']))
    except:
        return redirect('/member/login')
    ac = request.GET.get('account')
    trans = Transation.objects.filter(account=ac,user_idx=user.idx).all()
    # 만기일
    date = LProduct.objects.get(account=ac)
    remain = trans.filter(account=ac).last().remain
    context={
        'user':user,
        'trans':trans,
        'user':user,
        'date':date.date,
        'remain':remain
    }

    return render(request, 'loans_detail.html',context)
    




def checkMoney(request:HttpRequest):
    try: 
        user = User.objects.get(idx= int(request.session['login']))
    except:
        return redirect('/member/login')
    if request.method == 'GET':
        ac = request.GET.get('account')
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
    card = Card.objects.filter(user_idx=user_idx)
    context = {
        'user':user,
        'card':card
    }
    return render(request, 'send.html',context)





def check(request:HttpRequest):
    try: 
        user = User.objects.get(idx= int(request.session['login']))
    except:
        return redirect('/member/login')
    if request.method =='GET':
        myNum = request.GET.get('my_num')
        mypw = request.GET.get('outPw')
        mysm = request.GET.get('myMoney')
        num = request.GET.get('num')
        try: 
            take = Card.objects.get(account=num)
        except:
            error = None
            context ={
                'error':error
            }
            return HttpResponse(json.dumps(context), content_type="application/json")
        try:
            Card.objects.get(account=myNum, card_pw = mypw)
        except:
            error = '출금 정보가 일치하지 않습니다.'
            context ={
                'error':error
            }
            return HttpResponse(json.dumps(context), content_type="application/json")
        else:
            takeIdx = take.user_idx
            user = User.objects.get(idx=takeIdx.idx)
            name=user.name
            context= {
                'num':num,
                'name':name,
                'money':mysm,
            }   
            return HttpResponse(json.dumps(context), content_type="application/json") 







def sendMoney(request:HttpRequest):
    try: 
        user = User.objects.get(idx= int(request.session['login']))
    except:
        return redirect('/member/login')
    if request.method =='POST':
        # 보내는 사람 계좌번호
        myNum = request.POST.get('my_num')
        # 보내는 사람 돈
        mysm = request.POST.get('money')
        # 받는 사람 계좌번호
        num = request.POST.get('num')
        # 보내는이-------------------------------------
        # 보내는 사람 카드정보
        mycard = Card.objects.get(user_idx=user.idx,account=myNum)
        # 보내는 사람 카드이름
        card_name = CProduct.objects.get(card_idx = mycard.idx)
        # 보내고 계산하고 남은금액
        remain = mycard.remain - int(mysm)
        # 보내고 남은금액 업데이트
        Card.objects.filter(idx=mycard.idx).update(remain= remain)
        # 출금 0
        # 보내는이----------------------

        # 받는이----------------------
        # 받는 사람 카드정보
        take = Card.objects.get(account=num)
        # 받는 사람 카드idx
        takeIdx = take.idx
        print(takeIdx)
        # 받는 사람 받고 남은금액
        takeM = take.remain+int(mysm)
        # 받는 사람 
        takeUser= User.objects.get(idx=take.user_idx.idx)
        # 받는 사람 카드 이름
        take_card_name = CProduct.objects.get(card_idx = takeIdx)
        # 받는사람 입금 1   
        Card.objects.filter(idx=takeIdx).update(remain= takeM,last_date=dt.datetime.now().date())
        # user_idx = 보낸사람
        Transation.objects.create(kind=1,account=num,amount=mysm,remain=takeM,details=take_card_name.name,date=dt.datetime.now().date(),user_idx=user)
        # 출금 0
        # 보낸이 출금기록  user_idx = 받는사람
        Transation.objects.create(kind=0,account=myNum,amount=mysm,remain=remain,details=card_name.name,date=dt.datetime.now().date(),user_idx=takeUser)
        # 받는이----------------------
        context={
            'user':user,
            'name':takeUser.name,
            'mycard':mycard,
            'card_name':card_name,
            'money':mysm,
            'mymoney':remain
        }
    return render(request, 'send_suc.html',context)





def checkLoans(request:HttpRequest):
    try: 
        user = User.objects.get(idx= int(request.session['login']))
    except:
        return redirect('/member/login')
    if request.method == 'GET':
        ac = request.GET.get('account')
        my = LProduct.objects.get(user_idx=user.idx,account=ac)
        rate = my.rate
        limit = my.limited
        only_num = limit[-3::-1]
        if limit[-2] == '만':
            limit = only_num + '000000'
        else:
            limit = only_num + '00000000'
        inter = int(limit)
        rate = int(rate[:-1])
        # 납입할이자
        inter = (inter*(rate/100))/12

    context = {
        'account' : my.account,
        'kind' : my.kind,
        'name' : my.name,
        'time' : my.time,
        'rate' : my.rate,
        'limited' : my.limited,
        'remain' : my.remain,
        'date' : str(my.date),
        'inter' : inter,
    }
    return HttpResponse(json.dumps(context), content_type="application/json") 





def loans(request):
    try: 
        user = User.objects.get(idx= int(request.session['login']))
    except:
        return redirect('/member/login')
    user_idx = user.idx
    loans = LProduct.objects.filter(user_idx=user_idx)
    card = Card.objects.filter(user_idx=user_idx)
    context = {
        'user':user,
        'card':card,
        'loans':loans
    }
    return render(request, 'loans.html',context)





def sendLoans(request:HttpRequest):
    try: 
        user = User.objects.get(idx= int(request.session['login']))
    except:
        return redirect('/member/login')
    if request.method =='POST':
        ac = request.POST.get('my_num')
        l_ac = request.POST.get('l_num')
        pw = request.POST.get('outPw')
        inter = request.POST.get('inter')
        try:
            myAc = Card.objects.get(account=ac, card_pw=pw)
        except:
            error = '출금 정보가 일치하지 않습니다.'
            context ={
                'error':error
            }
            return redirect('/service/loans')
        loans = LProduct.objects.get(account=l_ac)
        l_remain = loans.remain - int(inter)
        c_remain = myAc.remain - int(inter)
        if c_remain < 0:
            error = '잔액이 부족합니다.'
            context = {
                'error':error
            }
            return redirect('/service/loans')
        else:
            # 납입자
            mycard = Card.objects.filter(account=ac,card_pw=pw).update(remain=c_remain,last_date=dt.datetime.now().date())
            card_name=CProduct.objects.get(card_idx=myAc.idx)
            Transation.objects.create(kind=0,account=ac,amount=int(inter),remain=c_remain,details=card_name.name,date=dt.datetime.now().date(),user_idx=user)
            # 대출납입
            LProduct.objects.filter(account=l_ac,user_idx=user.idx).update(remain=l_remain)
            loan_name=LProduct.objects.get(account=l_ac,user_idx=user.idx)
            Transation.objects.create(kind=1,account=l_ac,amount=int(inter),remain=l_remain,details=loan_name.name,date=dt.datetime.now().date(),user_idx=user)
            context={
                'user':user,
                'mycard':mycard,
                'loan_name':loan_name,
                'inter':inter,
            }
        return render(request, 'loans_suc.html',context) 





def deposit(request):
    try: 
        user = User.objects.get(idx= int(request.session['login']))
    except:
        return redirect('/member/login')
    
    deposit = Deposit.objects.filter(user_idx=user.idx).all()
    card = Card.objects.filter(user_idx=user.idx)
    context = {
        'user':user,
        'card':card,
        'dpo':deposit
    }

    return render(request, 'deposit.html',context)







def depositCheck(request:HttpRequest):
    print('------------등장--------------')
    try: 
        user = User.objects.get(idx= int(request.session['login']))
    except:
        return redirect('/member/login')
    if request.method == 'GET':
        ac = request.GET.get('account')
        my = Deposit.objects.get(user_idx=user.idx,deposit_num=ac)
        my_dpo = DProduct.objects.get(idx=my.d_product_idx.idx)
        limit = my_dpo.limited
        only_num = limit[-3::-1]
        if limit[-2] == '만':
            limit = only_num[::-1] + '0000'
            print(limit)
        else:
            limit = 0
        inter = int(limit)

    context = {
        'account' : ac,
        'dpo_num' : my.deposit_num,
        'kind' : my_dpo.kind,
        'name' : my_dpo.name,
        'time' : my_dpo.time,
        'rate' : my_dpo.rate,
        'limited' : my_dpo.limited,
        'remain' : my.remain,
        'date' : str(my.date),
        'limit_date' : str(my.limit_date),
        'inter' : inter,
    }
    return HttpResponse(json.dumps(context), content_type="application/json") 





def sendDeposit(request:HttpRequest):
    try: 
        user = User.objects.get(idx= int(request.session['login']))
    except:
        return redirect('/member/login')
    if request.method =='POST':
        ac = request.POST.get('my_num')
        d_ac = request.POST.get('d_num')
        pw = request.POST.get('outPw')
        inter = request.POST.get('inter')
        try:
            myAc = Card.objects.get(account=ac, card_pw=pw)
        except:
            error = '출금 정보가 일치하지 않습니다.'
            context ={
                'error':error
            }
            return HttpResponse(json.dumps(context), content_type="application/json") 
        deposit = Deposit.objects.get(deposit_num=d_ac)
        d_remain = deposit.remain + int(inter)
        c_remain = myAc.remain - int(inter)
        if c_remain < 0:
            error = '잔액이 부족합니다.'
            context = {
                'error':error
            }
            return HttpResponse(json.dumps(context), content_type="application/json") 
        else:
            # 납입자
            Card.objects.filter(account=ac,card_pw=pw).update(remain=c_remain,last_date=dt.datetime.now().date())
            card_name=CProduct.objects.get(card_idx=myAc.idx)
            Transation.objects.create(kind=0,account=ac,amount=int(inter),remain=c_remain,details=card_name.name,date=dt.datetime.now().date(),user_idx=user)
            # 적금납입
            Deposit.objects.filter(deposit_num=d_ac,user_idx=user.idx).update(remain=d_remain,date=dt.datetime.now().date())
            dpo=DProduct.objects.get(idx=deposit.d_product_idx.idx)
            Transation.objects.create(kind=1,account=d_ac,amount=int(inter),remain=d_remain,details=dpo.name,date=dt.datetime.now().date(),user_idx=user)
            context = {
                'deposit':deposit,
                'user':user,
                'dpo':dpo,
                'inter':inter
            }
        return render(request, 'deposit_suc.html',context)


def loss(request:HttpRequest):
    try: 
        user = User.objects.get(idx= int(request.session['login']))
    except:
        return redirect('/member/login')

    idx = user.idx
    card = Card.objects.filter(user_idx=idx)  # 보유 카드(여러개 가능)
    card_pct = CProduct.objects.all()

    context = {
        'user':user,
        # 'id' : id,
        'card': card,
        'card_pct': card_pct,
    }
        
    return render(request, 'loss.html', context)



def loss_detail(request:HttpRequest):
    try: 
        user = User.objects.get(idx= int(request.session['login']))
    except:
        return redirect('/member/login')

    idx = request.GET.get('loss')  # 선택한 카드의 idx
    card = Card.objects.get(idx=idx) # 선택한 카드의 카드정보
    card_pct = CProduct.objects.get(card_idx=idx)  # 선택한 카드의 카드상품정보


    context = {
        'user':user,
        'idx': idx,
        'card': card,
        'card_pct': card_pct,
    }
    return render(request, 'loss_detail.html', context)


def loss_suc(request:HttpRequest):
    try: 
        user = User.objects.get(idx= int(request.session['login']))
    except:
        return redirect('/member/login')
    idx_c = request.GET.get('loss_c') # 선택한 카드 idx
    idx_p = request.GET.get('loss_p') # 선택한 카드상품의 idx
    card_pct = CProduct.objects.get(idx=idx_p)
    loss_no = 1

    try: 
        Card.objects.filter(idx=idx_c).update(loss = loss_no)
        suc = "분실 신고가 완료 되었습니다."
        url = '/'
    except:
        suc = "오류가 발생했습니다. 다시 시도해주십시오."
        url = '/loss_detail/'




    context = {
        'user':user,
        'idx_c': idx_c,
        'idx_p': idx_p,
        'card_pct': card_pct,
        'suc': suc,
        'url': url,
    }

    return render(request, 'loss_suc.html', context)
    