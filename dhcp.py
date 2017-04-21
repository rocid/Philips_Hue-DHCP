#!/bin/python
import socket, struct, commands, time
from phue import Bridge
s = socket.socket( socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003) )

while(True):
	packet = s.recvfrom(65565)

	eth_protocol = struct.unpack('!6s6sH', (packet[0])[:14])
	if (eth_protocol[2] == 0x0800) :	
		ip_protocol = struct.unpack('!B', (packet[0])[23])
		ip_src = struct.unpack('!4s', (packet[0])[26:30])
		ip_dst = struct.unpack('!4s', (packet[0])[30:34])

		if (ip_protocol[0] == 17 and socket.inet_ntoa(ip_src[0]) == '0.0.0.0' and socket.inet_ntoa(ip_dst[0]) == '255.255.255.255') :
			udp_protocol_port = struct.unpack('!HH', (packet[0])[34:38])
			dhcp_type = struct.unpack('!B', (packet[0])[284])			
	
			if (udp_protocol_port[0] == 68 and udp_protocol_port[1] == 67 and dhcp_type[0] == 3) :
				dhcp_mac = struct.unpack('!6s', (packet[0])[288:294])
				dhcp_ip = struct.unpack('!4s', (packet[0])[296:300])
				print socket.inet_ntoa(dhcp_ip[0]) + ' ' + dhcp_mac[0].encode('hex')
				print 'Connecting...'
				
				b = Bridge('192.168.0.200')
				b.connect()
				b.set_light(1, 'on', True)
				b.set_light(2, 'on', True)
				b.set_light(3, 'on', True)

				b.lights[0].brightness = 100
				b.lights[1].brightness = 100
				b.lights[2].brightness = 100

				b.lights[0].xy = [0.2, 0.05]
				b.lights[1].xy = [0.2, 0.05]
				b.lights[2].xy = [0.2, 0.05]
				
				time.sleep(2)
				
				while(True):
					ping_com = commands.getoutput('ping -c 1 -w 1 ' + socket.inet_ntoa(dhcp_ip[0]))
					if ping_com.find('0 received') != -1:
						print 'Disconneting...'
						b.set_light(1, 'on', False)
						b.set_light(2, 'on', False)
						b.set_light(3, 'on', False)
						break
					
								

				
			 
		 
