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
        for a in answer:
            an.append(a['account'])
            am.append(a['amount'])
            re.append(a['remain'])
            de.append(a['details'])

        return (an,am,re,de)