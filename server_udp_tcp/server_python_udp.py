#Kelly Wang
#5351010
#Documentation: looked at socket python documentation and some stack overflow. 
#Did not take any code snipets 

import socket
import sys
import os

class UdpServer:
	def __init__(self, buffersize, filename):
		self.buffersize = buffersize
		self.filename = filename
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server_socket.bind(('', int(sys.argv[1])))

	def run(self):
		try:
			while True:
				self.receive_cmd()
				self.create_file()
				self.send_file()
				print("Successful file transmission.")
				self.server_socket.settimeout(None)
		except KeyboardInterrupt:
			self.server_socket.close()
			sys.exit(1)

	def recv(self):
		try:
			self.data, self.client_address = self.server_socket.recvfrom(self.buffersize)
			self.server_socket.sendto("ACK".encode(), self.client_address)
			self.data = self.data.decode()

		except socket.timeout:
			print(self.error_str, file=sys.stderr)
			sys.exit(1)

	def send(self):
		self.server_socket.sendto(self.data.encode(), self.client_address)
		for i in range(3):
			try:
				ack = self.server_socket.recvfrom(self.buffersize)[0].decode()
				if(ack == 'ACK'):
					break
			except socket.timeout:
				pass

	def receive_cmd(self):
		self.error_str = "Failed to receive instructions from the client."

		# get command length
		self.recv()
		self.cmd_len = int(self.data)

		# get command
		self.server_socket.settimeout(0.5)
		self.recv()
		self.cmd = self.data
		assert(len(self.cmd) == self.cmd_len)


	def create_file(self):
		index = self.cmd.find('>')
		if index != -1:
			cmd_temp = self.cmd.split('>')
			cmd_temp = cmd_temp[len(cmd_temp)-1]
			cmd_temp = cmd_temp.replace(" ", "")
			self.filename = cmd_temp
			os.system(self.cmd)
		else: # client does not specify file name
			self.filename = 'cmd.txt'
			os.system(cmd + ' > ' + self.filename)


	def send_file(self):
		self.server_socket.settimeout(1)

		# send file size
		f = open(self.filename, 'r')
		self.file_size = os.stat(self.filename).st_size
		self.error_str = "File transmission failed."
		self.data = str(self.file_size)
		self.send()

		# send file
		while True:
			read = f.read(self.buffersize)

			if not read:
				break

			# send length of data chunk
			self.data = str(len(read))
			self.send()

			# send data chunk
			self.data = read
			self.send()

		f.close()



if __name__ == '__main__':
	Server = UdpServer(512, 'udp_server_response.txt')
	Server.run()


# import socket
# import sys
# import os

# buffersize = 512

# def recv(server_socket, error_msg):
# 	try:
# 		data, client_address = server_socket.recvfrom(buffersize)
# 		server_socket.sendto("ACK".encode(), client_address)
# 		return data.decode(), client_address
# 	except socket.timeout:
# 		print(error_msg, file=sys.stderr)
# 		sys.exit(1)

# def send(server_socket, client_address, data, error_msg):
# 	server_socket.sendto(data, client_address)
# 	for i in range(3):
# 		try:
# 			ack = server_socket.recvfrom(buffersize)[0].decode()
# 			if(ack == 'ACK'):
# 				break
# 		except socket.timeout:
# 			pass

# def receive_cmd(server_socket):

# 	error_str = "Failed to receive instructions from the client."

# 	# get command length
# 	cmd_len, client_address = recv(server_socket, error_str)
# 	cmd_len = int(cmd_len)

# 	# get command
# 	server_socket.settimeout(0.5)
# 	cmd = recv(server_socket, error_str)[0]
# 	assert(len(cmd) == cmd_len)
# 	return cmd, client_address


# def create_file(cmd):
# 	index = cmd.find('>')
# 	if index != -1:
# 		cmd_temp = cmd.split('>')
# 		cmd_temp = cmd_temp[len(cmd_temp)-1]
# 		cmd_temp = cmd_temp.replace(" ", "")
# 		filename = cmd_temp
# 		os.system(cmd)
# 	else: # client does not specify file name
# 		filename = 'cmd.txt'
# 		os.system(cmd + ' > ' + filename)
# 	return filename


# def send_file(server_socket, filename, client_address):
# 	server_socket.settimeout(1)

# 	# send file size
# 	f = open(filename, 'rb')
# 	file_size = os.stat(filename).st_size
# 	error_str = "File transmission failed."
# 	send(server_socket, client_address, str(file_size).encode(), error_str)

# 	# send file
# 	while True:
# 		read = f.read(buffersize)

# 		if not read:
# 			break

# 		# send length of data chunk
# 		send(server_socket, client_address, str(len(read)).encode(), error_str)

# 		# send data chunk
# 		send(server_socket, client_address, read, error_str)

# 	f.close()


# def run():

# 	# create socket and bind
# 	server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# 	server_socket.bind(('', int(sys.argv[1])))

# 	while True:
# 	# receive command
# 		cmd, client_address = receive_cmd(server_socket)
# 		filename = create_file(cmd)
# 		send_file(server_socket, filename, client_address)
# 		print("finished sending file to client")

# if __name__ == '__main__':
# 	run()
