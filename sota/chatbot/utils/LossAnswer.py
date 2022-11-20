class LossAnswer:
    
    # Database 인스턴스 객체로 생성
    def __init__(self, db):
        self.db = db
        
    # 답변 검색
    def search(self,user_idx):          # l.search
        # 의도명, 개체명으로 답변 검색
        sql = self._make_query(user_idx)
        answer = self.db.select_all(sql)
        print(answer)
        # 검색되는 답변이 없으면 의도명만 검색
        if answer is None:
            sql = self._make_query(user_idx, None)
            answer = self.db.select_one(sql)
        cn=[]
        lo=[]
        pw=[]
        for a in answer:
            cn.append(a['card_num'])
            lo.append(a['loss'])
            pw.append(a['card_pw'])
        print(cn)
        print(lo)
        print(pw)
        return (cn,lo,pw)
        
    # 검색 쿼리 생성
    def _make_query(self, user_idx):
        sql = "select * from sota.card where user_idx ={}".format(user_idx)

        print(sql)
        return sql        
    