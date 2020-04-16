#Kelly Wang
#5351010
#Documentation: looked at socket python documentation and some stack overflow. 
#Did not take any code snipets 

import socket
import sys
import os


class TcpClient:
	def __init__(self, server, port, buffersize, filename, cmd):
		self.server = server
		self.port = port
		self.buffersize = buffersize
		self.filename = filename
		self.cmd = cmd
		self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	#add server response to file
	def recieve_file(self):
		try:
			f = open(self.filename, "wb")

			while True:
				data = self.client_socket.recv(buffersize)
				if(len(data) < 1):
					return
				f.write(data)

			f.close()
			print("File %s saved" %filename)

		except Exception:
			self.client_socket.close()
			print("Did not recieve response", file=sys.stderr)
			sys.exit(1)




	def run(self):
		try:
			self.client_socket.connect((self.server, self.port))

		except socket.error:
			print("Could not connect to server.", file=sys.stderr)
			sys.exit(1)

		try:
			self.client_socket.send(self.cmd.encode())
		except Exception:
			self.client_socket.close()
			print("Did not recieve response", file=sys.stderr)
			sys.exit(1)

		self.recieve_file()
		print("File %s saved."%filename)
		self.client_socket.close()

	def getPort(self):
		return self.port

if __name__ == '__main__':
		#request user server/port
	server = input("Enter server name or IP address: ")
	server = server.replace(" ", "")
	port = int(input("Enter port: "))
	if port < 0  or port > 65535:
	    print("Invalid port number.", file=sys.stderr)
	    sys.exit(1)

	#request usr cmd
	cmd = input("Enter command: ")
	index = cmd.find('>')
	if index != -1:
		cmd_temp = cmd.split('>')
		cmd_temp = cmd_temp[len(cmd_temp)-1]
		cmd_temp = cmd_temp.replace(" ", "")
		filename = cmd_temp

	else: #client does not specify file name
		filename = 'tcp_server_response.txt'

	Client = TcpClient(server, port, 512, filename, cmd)
	Client.run()

