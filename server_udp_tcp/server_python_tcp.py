#Kelly Wang
#5351010
#Documentation: looked at socket python documentation and some stack overflow. 
#Did not take any code snipets 

import socket
import sys
import os

class TcpServer:
	def __init__(self, buffersize, filename):
		self.buffersize = buffersize
		self.filename = filename
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server_socket.bind(('', int(sys.argv[1])))
		self.server_socket.listen(1)

	def run(self):
		try:
			while True:
				self.conn, self.address = self.server_socket.accept()

				self.create_file()
				self.send_file()
				print("File transmission successful")

		except KeyboardInterrupt:
			self.server_socket.close()
			sys.exit(1)

	def recieve_cmd(self):
		self.cmd = self.conn.recv(self.buffersize)
		if len(self.cmd) < 1:
			print("Failed to recieve instruction from the client.", file=sys.stderr)
			self.conn.close()
			sys.exit(1)
		return self.cmd.decode()

	def create_file(self):
		self.cmd = self.recieve_cmd()
		index = self.cmd.find('>')
		if index != -1:
			cmd_temp = self.cmd.split('>')
			cmd_temp = cmd_temp[len(cmd_temp)-1]
			cmd_temp = cmd_temp.replace(" ", "")
			self.filename = cmd_temp
			os.system(self.cmd)

		else: #client does not specify file name
			self.filename = 'cmd.txt'
			os.system(self.cmd + '>' + self.filename)
	

	def send_file(self):
		f = open(self.filename, 'rb')

		try:
			while True:
				read = f.read(self.buffersize)

				if not read:
					break
				self.conn.sendall(read)
		except socket.error:
			print("File transmission failed.", file=sys.stderr)
			sys.exit(1)
		f.close()
		self.conn.close()

if __name__ == '__main__':
	Server = TcpServer(512, 'tcp_server_response.txt' )
	Server.run()

