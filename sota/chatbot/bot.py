# 파이썬은 원래 기본적으로 한번에 하나의 쓰레드밖에 실행 못한다
# 'threading 모듈'을 통해 (내부적으로) 코드를 interleaving 방식으로 분할 실행함으로
# 멀티 쓰레딩 비슷(?)하게 동작시킨다.

import threading
import json

from config.DatabaseConfig import *
from utils.Database import Database
from utils.BotServer import BotServer
from utils.Preprocess import Preprocess
from models.intent.ProintentModel import ProintentModel
from models.intent.AllintentModel import AllintentModel
from models.intent.PayintentModel import PayintentModel
from models.ner.NerModel import NerModel
from utils.FindAnswer import FindAnswer
from bs4 import BeautifulSoup 
import requests



# 전처리 객체 생성
p = Preprocess(word2index_dic='train_tools/dict/sota2.bin',
               userdic='utils/ner.tsv')
p1=Preprocess(word2index_dic='train_tools/dict/sota3.bin',userdic='utils/ner.tsv')

# 의도 파악 모델
allIntent = AllintentModel(model_name='models/intent/all_intent_model.h5', preprocess=p)
proIntent = ProintentModel(model_name='models/intent/intent_product_model.h5', preprocess=p)
#payIntent = PayintentModel(model_name='models/intent/pay_intent_model.h5', preprocess=p)

# 개체명 인식 모델
ner = NerModel(model_name='models/ner/ner_when.h5', preprocess=p1)

# 클라리언트 요청을 수행하는 쓰레드 (에 담을) 함수
def to_client(conn, addr, params):
    db = params['db']
    
    try:
        db.connect()  
        
        # 데이터 수신
        read = conn.recv(2048)   # 수신 데이터가 있을 때까지 블로킹
        print('===========================')
        print('Connection from: %s' % str(addr))      
        
        if read is None or not read:
            # 클라이언트 연결이 끊어지거나, 오류가 있는 경우
            print('클라이언트 연결 끊어짐')
            exit(0)  # Thread 종료    
        
        # json 데이터로 변환
        recv_json_data = json.loads(read.decode())
        print("데이터 수신 : ", recv_json_data)
        query = recv_json_data['Query']  # 클라이언트로부터 전송된 질의어
        old=recv_json_data['old']
        if query=='처음으로':
            sent_json_data_str = {    # response 할 JSON 객체 준비
                "Query" : '안녕하세요',
                "Answer": '처음으로 가즈아',
                
                # "Intent": all_intent_name,
                # "Intent2":second_intent_name,
                # "NER": ner_predicts            
            }
            message = json.dumps(sent_json_data_str)
            conn.send(message.encode())  # responses

        if old=='None':
        # 전체 의도 파악
            all_intent_predict = allIntent.predict_class(query)
            all_intent_name = allIntent.labels[all_intent_predict]
            print(all_intent_predict)
            print(all_intent_name)
            print(old)
        
        
        # 상품조회 의도 파악
        #pro_intent_predict = proIntent.predict_class(query)
        #pro_intent_name = proIntent.labels[pro_intent_predict]
        
        # 상환 및 납부 의도 파악
        #pay_intent_predict = payIntent.predict_class(query)
        #pay_intent_name = payIntent.labels[pay_intent_predict]

        # 개체명 파악
        #ner_tags = ner.predict_tags(query)
        ner_predicts=None
        ner_tags=None
        second_intent_name=None
        if old!='None':
            all_intent_name=old

        if all_intent_name=='상품':



            
            sp=proIntent.predict_class(query)
            second_intent_name=proIntent.labels[sp]
            print(second_intent_name)
            

            if recv_json_data['Query'] =='적금상품':
                pd=''
                f = FindAnswer(db)
                result=f.selectdepoist()
                print(result)
                if recv_json_data['Query']=='적금상품':
                    pd=recv_json_data['Query']
                elif second_intent_name=='적금상품':
                    pd=second_intent_name
                

                
                sent_json_data_str={
                    'answer': '아~{}을 원해?'.format(pd),
                    "url":result,
                    "old":"{}".format(pd)
                    
                }
                message = json.dumps(sent_json_data_str)
                conn.send(message.encode())  
            
            elif recv_json_data['Query'] == '대출상품':
                
                f = FindAnswer(db)
                result=f.selectloan()
                print(result)
                pd=''
                if recv_json_data['Query']=='대출상품':
                    pd=recv_json_data['Query']
                elif second_intent_name=='대출상품':
                    pd=second_intent_name
                

                print(pd)
                sent_json_data_str={
                    "answer": '아~{}을 원해?'.format(pd),
                    "url":result,
                    "old":"{}".format(pd)
                    
                }
                print(sent_json_data_str)
                message = json.dumps(sent_json_data_str)
                conn.send(message.encode())  
            
            elif recv_json_data['Query'] =='카드상품':
                
                f = FindAnswer(db)
                result=f.selectcard()
                print(result)
               
                pd=recv_json_data['Query']
                

                
                sent_json_data_str={
                    'answer': '아~{}을 원해?'.format(pd),
                    "url":result,
                    "old":"{}".format(pd)
                    
                }
                message = json.dumps(sent_json_data_str)
                conn.send(message.encode())  
            try:
                f = FindAnswer(db)
                answer_text, answer_image = f.search(all_intent_name,second_intent_name, ner_tags)
                answer = f.tag_to_word(ner_predicts, answer_text)            
            except:
                answer = "죄송해요 무슨 말인지 모르겠어요. 조금 더 공부 할게요."
                answer_image = None
            if second_intent_name =='대출상품':
                f = FindAnswer(db)
                result=f.selectloan()
                answer_image=result
            sent_json_data_str = {    # response 할 JSON 객체 준비
                "Query" : query,
                "Answer": answer,
                "AnswerImageUrl" : answer_image,
                "Intent": all_intent_name,
                "Intent2":second_intent_name,
                "NER": ner_predicts            
            }
            message = json.dumps(sent_json_data_str)
            conn.send(message.encode())  # responses

        elif all_intent_name=='조회':
            print('여긴 조회야')
            recv_json_data['old']=all_intent_name
            old=recv_json_data['old']
            
            
            ner_predicts = ner.predict(query)
            ner_tags = ner.predict_tags(query)
            print(ner_tags)
            print(ner_predicts)
            result=''
            
            
            # for ne in ner_predicts:
            #     if(ne[2]=='o'):
            #         f = FindAnswer(db)  
            #         answer_text, answer_image = f.search(all_intent_name,second_intent_name, ner_tags)
            #         answer = f.tag_to_word(ner_predicts, answer_text) 
                        
            # sent_json_data_str = {    # response 할 JSON 객체 준비
            #     "Query" : query,
            #     "Answer": answer,
            #     "Intent": all_intent_name,
            #     "Intent2":second_intent_name,
            #     "old":old,
            #     "NER": ner_predicts,
            #     'result':result
            # }
            # message = json.dumps(sent_json_data_str)
            # conn.send(message.encode())  # resp
            # 답변 검색
            try:
                f = FindAnswer(db)
                day=ner_predicts[0][0][:2]
                result=f.tran(day,1)
                answer_text, answer_image = f.search(all_intent_name,second_intent_name, ner_tags)
                answer = f.tag_to_word(ner_predicts, answer_text)            
            except:
                answer = "죄송해요 무슨 말인지 모르겠어요. 조금 더 공부 할게요."
                answer_image = None
                
            sent_json_data_str = {    # response 할 JSON 객체 준비
                "Query" : query,
                "Answer": answer,
                "Intent": all_intent_name,
                "Intent2":second_intent_name,
                "old":old,
                "NER": ner_predicts,
                'result':result
            }
            message = json.dumps(sent_json_data_str)
            conn.send(message.encode())  # responses
            
        elif all_intent_name=='이체':# 이체 할래/ 얼마 이체할래 
            print('여긴 이체')
            card=''
            recv_json_data['old']=all_intent_name
            old=recv_json_data['old']
            print('여기까진 된거야')
            # print(len(recv_json_data['Query']))
            # if len(recv_json_data['Query'])==16:
            #     myac=recv_json_data['Query']
            #     sent_json_data_str = {    # response 할 JSON 객체 준비
                
            #     "Answer": '얼마를 어디에 보낼래?',
            #     "myac":myac,
            #     "Intent": all_intent_name,
            
            #     "old":old,
                
                         
            #     }
            #     print(sent_json_data_str)
            #     message = json.dumps(sent_json_data_str)
            #    conn.send(message.encode())  # responses
            if '3' in recv_json_data['Query']: #ner태그가 아무것도 안걸리면 
                m=recv_json_data['Query'][1]
                t=recv_json_data['Query'][2]
                a=recv_json_data['Query'][3]
                f=FindAnswer(db)
                result=f.substract(m,t,a,1)
                print(result)
                sent_json_data_str = {  
                    "answer": '이체 완료',
                    "url": '확인할 수 있는 창'
                }
                print('뭐가 문제야 섬띵')

                message = json.dumps(sent_json_data_str)
                conn.send(message.encode())  # responses
                
            try:
            
                f = FindAnswer(db)
                card=f.card(1)
            
                
                answer_text, answer_image = f.search(all_intent_name,second_intent_name, ner_tags)
                answer = f.tag_to_word(ner_predicts, answer_text)            
            except:
                answer = "죄송해요 무슨 말인지 모르겠어요. 조금 더 공부 할게요."
                answer_image = None
            
            sent_json_data_str = {    # response 할 JSON 객체 준비
                "Query" : query,
                "Answer": answer,
                "AnswerImageUrl" : answer_image,
                "Intent": all_intent_name,
                #"result":[money,account],
                "old":old,
                "NER": ner_predicts,
                "card":card           
            }
            message = json.dumps(sent_json_data_str)
            conn.send(message.encode())  # responses

        try:
            f = FindAnswer(db)
            
            answer_text, answer_image = f.search(all_intent_name,second_intent_name, ner_tags)
            answer = f.tag_to_word(ner_predicts, answer_text)            
        except:
            answer = "죄송해요 무슨 말인지 모르겠어요. 조금 더 공부 할게요."
                           
        result='' 
        sent_json_data_str = {    # response 할 JSON 객체 준비
                "Query" : query,
                "Answer": answer,
                "Intent": all_intent_name,
                "Intent2":second_intent_name,
                "old":old,
                "NER": ner_predicts ,
                'result':result
            }
        message = json.dumps(sent_json_data_str)
        conn.send(message.encode())  # responses
            
            
        
    except Exception as ex:
        print(ex)
        
    finally:
        if db is not None:
            db.close()
        conn.close()   # 응답이 끝나면 클라이언트와의 연결(클라이언트 소켓) 도 close 해야 한다
    
if __name__ == '__main__':

    # 질문/답변 학습 디비 연결 객체 생성
    db = Database(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db_name=DB_NAME
    )
    print("DB 접속")

    # ① 챗봇 소켓 서버 생성
    port = 5050   # 서버의 통신포트
    listen = 100    # 최대 클라이언트 연결수

    # 봇 서버 동작
    bot = BotServer(port, listen)
    bot.create_sock()
    print("bot start")
    
    while True:
        conn, addr = bot.ready_for_client()  # client 요청 대기하다가 연결 수락!
        
        params = {
            "db": db,
        }
        
        client = threading.Thread(target=to_client, args=(conn, addr, params))
        client.start()   # 쓰레드 시작











