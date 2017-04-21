#!/bin/python
#-*- coding: utf-8 -*-
import socket, select, string, sys

# 입력할수 있는 폼 
def prompt() :
    sys.stdout.write('\n<You> ')
    sys.stdout.flush()
 
if __name__ == "__main__":
     
    if(len(sys.argv) < 3) :
        print 'Usage : python telnet.py hostname port'
        sys.exit()
     
    host = sys.argv[1]
    port = int(sys.argv[2])
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
     
    # connect 예외처리
    try :
        s.connect((host, port))
    except :
        print 'Unable to connect'
        sys.exit()
     
    print 'Connected to remote host. Start sending messages'
    prompt()
     
    while 1:
        socket_list = [sys.stdin, s]
         
        # 읽을 수 있는 소켓만 가져옴
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
         
        for sock in read_sockets:
	    # timeout을 통해 데이터가 없을때 연결을 끊음
            if sock == s:
                data = sock.recv(4096)
                if not data :
                    print '\nDisconnected from chat server'
                    sys.exit()
                else :
                    sys.stdout.write(data)
                    prompt()
            # 아닐경우 정상적으로 데이터를 주고받음
            else :
                msg = sys.stdin.readline()
                s.send(msg)
                prompt()

