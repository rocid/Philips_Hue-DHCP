#!/bin/python
#-*- coding: utf-8 -*-
import socket, select

# 모든 소켓에 메세지를 보내기 위한 함수
def broadcast_data (sock, message):
    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
		# ctrl + c를 넣을때 소켓을 지우는 기능을 함
                socket.close()
                CONNECTION_LIST.remove(socket)

if __name__ == "__main__":
        
    CONNECTION_LIST = [] # 소켓리스트를 저장하기 위한 변수
    RECV_BUFFER = 4096 # 최대 버퍼의 크기
    PORT = 5000 # 포트번호
  
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('', PORT))
    server_socket.listen(10)
 
    # 소켓리스트를 저장함
    CONNECTION_LIST.append(server_socket)
 
    print "Chat server started on port " + str(PORT)
 
    while 1:
	
	# select를 통해 read_socket - 정상적인 소켓들을 CONNECTION_LIST를 저장
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
 
        for sock in read_sockets:
            # 처음 연결할때 
            if sock == server_socket:
		# 서버 소켓을 통해 새로운 연결을 한 경우 서버에 addr과 주소를 출력함
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                print "Client (%s, %s) connected" % addr
                # 새로운 사용자가 들어왔음을 이미 있는 소켓들에게 알림 
                broadcast_data(sockfd, "[%s:%s] entered room\n" % addr)
             
	    # 클라이언트에서 메세지가 왔을때
            else:
		# client를 통해 받은 테이터를 처리
                try:
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        broadcast_data(sock, "\r" + '<' + str(sock.getpeername()) + '> ' + data)                 
                except:
                    broadcast_data(sock, "Client (%s, %s) is offline" % addr)
                    print "Client (%s, %s) is offline" % addr
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue
     
    server_socket.close()

