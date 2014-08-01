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
from pymouse import PyMouse, PyMouseEvent


HOST = '10.176.127.252'                 # Enter the IP of the remote host within Quotes

PORT = 5009              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
msg='Hi'
s.send(msg.encode('utf-8'))
m = PyMouse()
ck={}
while 1:
	data=s.recv(11)
	if data:
		msg=repr(data)
		
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
			if(msg[0]=='b'):
				print(msg1)
				msg1=msg1[1:len(msg1)-1]
				msg=msg+msg1
			msg=msg[:len(msg)-1]
		try:
			a=msg.find(',')
			x=int(msg[:4])
			y=int(msg[4+1:9])
			m.move(x,y)
			
			if len(msg)==10 and msg[4]==',' and not int(msg[9])==0 and not int(msg[9])>3:
			
				try:
					clk = ck[int(msg[9])]
					m.release(x,y,ck[int(msg[9])])
					ck.pop(int(msg[9]))
			
				except:
					ck[int(msg[9])]=int(msg[9])
					try:
						m.press(x,y,int(msg[9]))
					except:
						#Cannot Press out of bounds
						print('Cannot Press out of bounds')
			
		except ValueError:
			print (msg)
s.close()
