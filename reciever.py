#    Copyright (C) 2013  Ranjith Kumar S
#    
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


# Client program
import socket
from pymouse import PyMouse


HOST = ''                 # Enter the IP of the remote host within Quotes

PORT = 50007              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
msg='Hi'
s.send(msg.encode('utf-8'))
m = PyMouse()
ck=0
while 1:
	data=s.recv(11)
	if data:
		msg=repr(data)
		#print(msg)
		if msg[len(msg)-2]=='!':
			if(msg[0]=='b'):
				st=2
			else:
				st=1
			msg=msg[st:len(msg)-2]
		else:
			print(msg)
			if(msg[0]=='b'):
				st=2
			else:
				st=1
			msg=msg[st:len(msg)-1]
			print(msg)
			while len(msg)<11:
				rem_b=11-len(msg)
				data=s.recv(rem_b)
				msg1=repr(data)
				print(msg1)
				msg1=msg1[1:len(msg1)-1]
				msg=msg+msg1
			msg=msg[:len(msg)-1]
		try:
			a=msg.find(',')
			x=int(msg[:4])
			y=int(msg[4+1:9])
			m.move(x,y)
			if not int(msg[9])==ck:
				if ck == 0:
					#Button Pressed
					# 0 -> 1 signifies Press
					if int(msg[9])==1:
						m.press(x,y,int(msg[9]))
				else:
					#Button Released
					# 1-> 0 signifies release
					if ck == 1 and int(msg[9]) == 0:
						m.release(x,y)
					else:
						m.click(x,y,ck)
				ck = int(msg[9])
		except ValueError:
			print (msg)
s.close()
