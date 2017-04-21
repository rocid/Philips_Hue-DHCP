#!/bin/python
import socket, select, string, sys
from phue import Bridge

b = Bridge('192.168.0.200')
b.connect()

if __name__ == "__main__":

    if(len(sys.argv) < 3) :
        print 'Usage : python telnet.py hostname port'
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    try :
        s.connect((host, port))
    except :
        print 'Unable to connect'
        sys.exit()

    print 'Connected to remote host. Start sending messages'
	
    while 1:
        socket_list = [sys.stdin, s]

        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])

        for sock in read_sockets:
            if sock == s:
                data = sock.recv(4096)
				list = data.split()
                if not data :
                	print '\nDisconnected from chat server'
                	sys.exit()
            elif len(list) == 8:
				if list[3]=='qwer':
					s.send('pass Error')
				else:
					if int(list[4])==1:
						b.set_light(int(list[3]), 'on', True)
						print(list[3] + ' light on')
						s.send(list[3] + ' light on')
					else:
						b.set_light(int(list[3]), 'on', False)
						print(list[3] + ' light off')
						s.send(list[3] + ' light off')

					b.lights[int(list[3]) - 1].brightness = int(list[5])
					print(list[3] + ' light bright : ' + list[5])
					s.send(list[3] + ' light bright : ' + list[5])

					b.lights[int(list[3]) - 1].xy = [float(list[6]), float(list[7])]
					print(list[3] + ' light color : [' + list[6] + ', ' + list[7] + ']')
					s.send(list[3] + ' light color : [' + list[6] + ', ' + list[7] + ']')
 
					print(list[3] + ' light State Change')
					s.send(list[3] + ' light State Change')
 
			else:
				sys.stdout.write(data)							

