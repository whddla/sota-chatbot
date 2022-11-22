class FindAnswer:
    
    # Database 인스턴스 객체로 생성
    def __init__(self, db):
        self.db = db
        
    # 답변 검색
    def search(self, intent_name, second_intent_name,ner_tags):
        # 의도명, 개체명으로 답변 검색
        sql = self._make_query(intent_name,second_intent_name, ner_tags)
        answer = self.db.select_one(sql)
        print(answer)
        # 검색되는 답변이 없으면 의도명만 검색
        if answer is None:
            sql = self._make_query(intent_name,second_intent_name=None,ner_tags=None)
            answer = self.db.select_one(sql)

        return (answer['answer'], answer['answer_image'])
        
    
    # 검색 쿼리 생성
    def _make_query(self, intent_name, second_intent_name,ner_tags):
        sql = "select * from sota.chatbot_train_data"
        
        # intent_name 만 주어진 경우
        if intent_name != None and second_intent_name == None and ner_tags==None:
            sql = sql + " where intent='{}' ".format(intent_name)
            print(1)
        
        elif intent_name!= None and second_intent_name !=None:
            sql=sql+ " where intent='{}'".format(intent_name) + " and ner='{}' ".format(second_intent_name)
            print(2)
        # intent_name 과 개체명도 주어진 경우
        elif intent_name != None and second_intent_name == None and ner_tags != None:
            where = ' where intent="%s" ' % intent_name
            if (len(ner_tags) > 0):
                where += 'and ('
                for ne in ner_tags:
                    where += " ner like '%{}%' or ".format(ne)
                where = where[:-3] + ')'
            sql = sql + where

        # 동일한 답변이 2개 이상인 경우, 랜덤으로 선택
        #sql = sql + " order by rand() limit 1"
        print(sql)
        return sql        
    
    # NER 태그를 실제 입력된 단어로 변환
    def tag_to_word(self, ner_predicts, answer):
        if ner_predicts == None:
            return answer

        for word, tag in ner_predicts:
            
            # 변환해야하는 태그가 있는 경우 추가
            if tag == 'b_st' or tag == 'b_end':
                answer = answer.replace(tag, word)  # 태그를 입력된 단어로 변환
                
        answer = answer.replace('{', '')
        answer = answer.replace('}', '')
        return answer
    def tag_to_word2(self, ner_predicts, answer):
        if ner_predicts == None:
            return answer

        for word, tag in ner_predicts:
            
            # 변환해야하는 태그가 있는 경우 추가
            if tag == 'B_account' or tag == 'B_money':
                answer = answer.replace(tag, word)  # 태그를 입력된 단어로 변환
                
        answer = answer.replace('{', '')
        answer = answer.replace('}', '')
        return answer


    def findtran(self,day,user_idx):
        sql = "select * from sota.transation"+" where date='2022-11-{}'".format(day)+ " and user_idx={}".format(user_idx)
        print(sql)
        return sql

    def tran(self,day,user_idx):
        sql = self.findtran(day,user_idx)
        print(sql)
        answer = self.db.select_all(sql)
        an=[]
        am=[]
        re=[]
        de=[]
        ki=[]
        for a in answer: 
            an.append(a['account'])
            am.append(a['amount'])
            re.append(a['remain'])
            de.append(a['details'])
            if a['kind']==0:
                ki.append('출금')
            else:
                ki.append('입금')
            

        return (ki,an,am,re,de)

    def findcard(self,user_idx):
        print('findcard')
        sql="select * from sota.card" + " where user_idx={}".format(user_idx) 
        print(sql)
        return sql
    
    def card(self,user_idx):
        print('card접속1')
        sql=self.findcard(user_idx)
        print('card접속2')
        answer=self.db.select_all(sql)

        myac=[]
        for a in answer:
            myac.append(a['account'])
        return myac

    def substract(self,m,t,a,user_idx):
        
        t=str(t)
        a=str(a)
        m=int(m)
        sql = "select * from sota.transation"+" where user_idx={}".format(user_idx)+" and account='{}'".format(a)+" ORDER BY idx DESC LIMIT 1"
        answer=self.db.select_one(sql)
        
        
        print(answer['remain'])
        balance=int(answer['remain'])-m
        sql= "select * from sota.transation"+" where account='{}'".format(t)+" ORDER BY idx DESC LIMIT 1"
        answer1=self.db.select_one(sql)
        print(answer1,answer)
        t_idx=answer1['user_idx']
        earn=answer1['remain']+m
        print(earn)
        #add1="insert into sota.transation (kind,account,amount,remain,details,date,user_idx)"+" values (%d,%s,%d,%d,%s,%s,%d)"
        add1="insert into sota.transation (kind,account,amount,remain,details,date,user_idx)"+" values ({},'{}',{},{},'{}','{}',{})".format(0,a,m,balance,t,'2022-11-19',user_idx)
        print(add1)
        add2="insert into sota.transation (kind,account,amount,remain,details,date,user_idx)"+" values ({},'{}',{},{},'{}','{}',{})".format(1,t,m,earn,a,'2022-11-19',user_idx)
        #add1_w=(0,a,m,balance,t,'2022-11-19',user_idx)
        print('여긴되겠지 그럼')
        ex=self.db.execute(add1)
        ex=self.db.execute(add2)
        
        #ex.execute(add1,add1_w)
        print('역시 너냐')

        return balance

    def selectdepoist(self):
        sql="select * from sota.d_product"
        answer=self.db.select_one(sql)
        result=answer['name']
        print(result)
        return result

        
    
    def selectdepoist(self):
        sql="select * from sota.d_product"
        answer=self.db.select_all(sql)

        name=[]
        limited=[]
        time=[]
        rate=[]
        kind=[]
        for a in answer:
            name.append(a['name'])
            limited.append(a['limited'])
            time.append(a['time'])
            rate.append(a['rate'])
            kind.append(a['kind'])


        
        return (name,limited,time,rate,kind)

        
    
    def selectloan(self):
        sql="select * from sota.l_product"
        answer=self.db.select_all(sql)
        name=[]
        limited=[]
        time=[]
        rate=[]
        kind=[]
        for a in answer:
            name.append(a['name'])
            limited.append(a['limited'])
            time.append(a['time'])
            rate.append(a['rate'])
            kind.append(a['kind'])


        
        return (name,limited,time,rate,kind)


    def selectcard(self):
        sql="select * from sota.c_product"
        answer=self.db.select_all(sql)
        name=[]
        ben=[]
        for a in answer:
            name.append(a['name'])
            ben.append(a['benefit'])

        return (name,ben)
    def findpw(self,user_idx):
        sql="select * from sota.card where user_idx={}".format(user_idx)

        answer=self.db.select_all(sql)
        pw=[]
        for a in answer:
            pw.append(a['card_pw'])
        
        return pw
