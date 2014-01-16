
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

# Echo server program
import socket
import time
from pymouse import PyMouse, PyMouseEvent

# Global Variables
ck=0

# For click Detection
class ClickEventListener(PyMouseEvent):
	def click(self, x, y, button, press):
		global ck
		if press:
			ck = button
		else:
			ck = 0


# Symbolic name meaning the local host
HOST = ''   			  #IP Number '' Mentioning its a localhost
print (HOST)
PORT = 5009             # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))

print('going to connect')
s.listen(1)
conn, addr = s.accept()
print("connected to")
print(addr)

#Initialising Variables
ck=0
d=0
msg = conn.recv(1024)
old_msg=''

#Extend Screen Side
#if you Extended your screen on the right Give flag as 1
#if you Extended your screen on the left Give flag as 0
flag=0

#Initialising PyMouse
m = PyMouse()
sc_len,sc_wid = m.screen_size()

#Initializing Click Listeners
m1 = ClickEventListener()
m1.start()

while 1:
	#----------Mouse ---------------
	# This Detects the Mouse, and whether click is happening, basically for all mouse related stuff
	
	x, y = m.position()
	
	#For the client on the left side of the server ( Monitor extended on the left)
	if flag == 0 and x > sc_len:
		d=x
		flag=1
	
	if x>=(sc_len-1):
		x=abs(sc_len-1-abs(x-d))
		msg=str(str("%04d"%x)+','+str("%04d"%y)+str(ck)+'!')
		if msg == old_msg:
			continue
		old_msg=msg
		conn.send(msg.encode('utf8'))
		time.sleep(0.000001)
		print ck
		clk=ck
conn.close()
