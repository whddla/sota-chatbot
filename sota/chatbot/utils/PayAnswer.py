from . import Database

class PayAnswer:
    
    # Database 인스턴스 객체로 생성
    def __init__(self, db):
        self.db = db
        
    # 답변 검색
    def search_ans(self, intent_name, second_intent_name):
        # 의도명1, 의도명2 로 답변 검색
        sql = self.intent_make_query(intent_name, second_intent_name) #
        answer = self.db.select_one(sql)
        # 검색되는 답변이 없으면 의도명만 검색
        if answer is None:
            sql = self.intent_make_query(intent_name, None)
            answer = self.db.select_one(sql)

        return (answer['answer'], answer['answer_image'])  # 답변
        



    def search_user(self, user_idx):          # 공인인증서 번호
        # 로그인한 세션의 user_idx 로 검색
        sql = self.user_make_query(user_idx)
        answer = self.db.select_all(sql)
        # 검색되는 답변이 없으면 의도명만 검색
        if answer is None:
            sql = self.user_make_query(user_idx, None)
            answer = self.db.select_one(sql)

        return answer['p_pw']  # 공인 인증서 번호 반환


    def search_card(self, user_idx):          # 입출금 계좌번호, 가용한 잔여금액
        # 로그인한 세션의 user_idx 로 검색
        sql = self.card_make_query(user_idx)
        answer = self.db.select_all(sql)
        # user_idx에 할당된 모든 데이터 가져옴
        if answer is None:
            sql = self.card_make_query(user_idx, None)
            answer = self.db.select_one(sql)
        account = []
        remain = []
        for one in answer:
            account.append(one['account'])
            remain.append(one['remain'])

        return (account, remain)
        # return (answer['account'], answer['remain'])
        # index {0: 입출금 계좌번호, 1: 계좌에 남은금액(납입가능한 금액)}


    def search_loan(self, user_idx):          # 가입한 대출상품정보
            # 로그인한 세션의 user_idx 로 검색
            sql = self.loan_make_query(user_idx)
            answer = self.db.select_all(sql)
            # 검색되는 답변이 없으면 의도명만 검색
            if answer is None:
                sql = self.loan_make_query(user_idx, None)
                answer = self.db.select_one(sql)

            name=[]
            limited=[]
            rate=[]
            account=[]
            date=[]
            remain=[]
            for one in answer:
                name.append(one['name'])
                limited.append(one['limited'])
                date.append(one['date'])
                rate.append(one['rate'])
                account.append(one['account'])
                remain.append(one['remain'])
            
            return (name, limited, date, rate, account, remain)
            # return (answer['name'], answer['limited'], answer['rate'], answer['account'], answer['date'], answer['remain'])
            # index {0: 상품명, 1: 한도, 2: 이율, 3: 거래금액, 4: 만기, 5: 갚아야할 금액}


    def search_deposit(self, user_idx):          # 가입한 적금  # deposit table
            # 로그인한 세션의 user_idx 로 검색
            sql = self.deposit_make_query(user_idx)
            answer = self.db.select_all(sql)
            # 검색되는 답변이 없으면 의도명만 검색
            if answer is None:
                sql = self.deposit_make_query(user_idx, None)
                answer = self.db.select_one(sql)

            deposit_num=[]
            date=[]
            remain=[]
            limit_date=[]
            d_product_idx=[]
            d_name=[]
            for one in answer:
                deposit_num.append(one['deposit_num'])
                date.append(one['date'])
                remain.append(one['remain'])
                limit_date.append(one['limit_date'])
                d_product_idx.append(one['d_product_idx'])
                d_name.append(one['d_name'])

            return (deposit_num, date, remain, limit_date, d_product_idx, d_name)
            # index {0: 적금계좌번호 idx 1: 가입 날짜, 2: 적금누적금액, 3: 적금만기날짜, 4: 적금상품idx, 5: 적금상품명}


    def search_deposit_p(self, d_product_idx):          # 가입한 적금 상품(d_product)  # 위 함수에서 answer['d_product_idx'] 받아오기....
            # 로그인한 세션의 user_idx 로 검색
            sql = self.depo_make_query(d_product_idx)
            answer = self.db.select_all(sql)
            # 검색되는 답변이 없으면 의도명만 검색
            if answer is None:
                sql = self.depo_make_query(d_product_idx, None)
                answer = self.db.select_one(sql)
            
            idx =[]
            limited=[]
            time=[]
            rate=[]
            name=[]
            for one in answer:
                idx.append(one['idx'])
                limited.append(one['limited'])
                time.append(one['time'])
                rate.append(one['rate'])
                name.append(one['name'])

            return (idx, name, limited, time, rate)
            # index {0: 적금상품 idx 1: ,적금상품명, 2: 적금 한도, 3: 적금기간, 4: 이율}


        
        



    ###############################################   
    #  
    
    # 답변검색 쿼리 생성
    def intent_make_query(self, intent_name, second_intent_name):
        sql = "select * from chatbot_train_data"
        
        # all_intent_Model + pay_intent_Model
        if intent_name != None and second_intent_name != None:
            where = ' where intent="%s" ' % intent_name
            where += 'and ( ner = "'
            if second_intent_name == 0:
                ner = "납부"
            elif second_intent_name == 1:
                ner = "대출"
            else:
                ner = "적금"
            where += ner + '")'
            sql = sql + where

        return sql        



    # user 검색 쿼리 생성
    def user_make_query(self, user_idx):
        sql = "select * from user"
        sql = sql + " where idx='{}' ".format(user_idx)
            
        return sql  


    # 입출금 계좌번호 검색 쿼리 생성
    def card_make_query(self, user_idx):
        sql = "select * from card  where user_idx={}".format(user_idx)
            
        return sql 


    # 가입된 대출상품 검색 쿼리 생성
    def loan_make_query(self, user_idx):
        sql = "select * from l_product"
        sql = sql + " where user_idx='{}' ".format(user_idx)
            
        return sql 

    # 가입된 적금 검색 쿼리 생성
    def deposit_make_query(self, user_idx):
        sql = "select * from deposit"
        sql = sql + " where user_idx='{}' ".format(user_idx)
       
        return sql 
    
    
    # 적금 상품 검색 쿼리 생성
    def depo_make_query(self, d_product_idx):
        sql = "select * from D_product"
        sql = sql + " where idx='{}' ".format(d_product_idx)
        
        return sql 

    # 거래 검색 쿼리 생성?
    # def trans_make_query(self, user_idx):
    #     sql = "select * from transaction"
    #     sql = sql + " where user_idx='{}' ".format(user_idx)
        
    #     # 동일한 답변이 2개 이상인 경우, 랜덤으로 선택
    #     #sql = sql + " order by rand() limit 1"
    #     return sql