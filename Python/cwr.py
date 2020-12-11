#Reminder: THis is a comment. The first line imports a default library "socket" into python.
#You do not install this. The second line is initialization to add TCP/IP protocol to the endpoint.
import socket
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Assigns a port for the server tha listens to clients connecting to this port
serv.bind(('0.0.0.0',8080))
serv.listen(5)
while True:
	conn, addr = serv.accept()
	from_client = ''
	while True:
		data = conn.recv(4096)
		if not data: break
		#from_client += data
		#print(from_client)
		print(data)
		#output = 'I am SERVER\n'
		#conn.send(b'I am SERVER\n')
	conn.close()
	print('client disconnected')
