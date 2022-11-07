import socket    # 파이썬에서 제공하는 저수준 네트워킹 인터페이스 API

class BotServer:
    # ① 생성자: 포트번호, 동시연결 클라이언트수를 멤버변수로 저장
    def __init__(self, srv_port, listen_num):
        self.port = srv_port
        self.listen = listen_num
        self.mySock = None  

    # ② TCP/IP socket 생성
    # 지정한 서버포트(port)로 지정한 연결수(listen) 만큼 클라이언트 연결을 수락하도록 합니다        
    def create_sock(self):
        self.mySock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mySock.bind(("0.0.0.0", int(self.port))) # 0.0.0.0 : 로컬시스템의 모든 IPv4 주소
        self.mySock.listen(int(self.listen))
        return self.mySock
    
    # ③ client 대기
    # 챗봇 클라이언트 연결을 대기하고 있다가 연결을 수락하는 메소드
    # 서버 소켓은 우리가 설정한 주소와 통신에 바인드되어 클라이언트 연결을 리스닝(listening) 하고 있게 된다
    # 클라이언트가 연결을 요청하는 즉시 accept() 함수는 클라이언트와 통신할  있는
    # 클라이언트 소켓 객체를 리턴하게 됩니다.  
    # 이때 리턴값은!  (conn, address) 튜플입니다
    #   conn : 연결된 챗봇 클라이언트의 데이터를 '송수신' 할수 있는 '클라이언트 소켓'입니다
    #   address : 연결된 챗봇 클라이언트 소켓의 바인드된 주소입니다    
    def ready_for_client(self):
        return self.mySock.accept()
    
    # ④ 현재 생성된 '서버 socket' 반환
    def get_sock(self):
        return self.mySock    
        