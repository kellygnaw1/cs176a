#Kelly Wang
#5351010
#Documentation: looked at socket python documentation and some stack overflow. 
#Did not take any code snipets 

import socket
import sys
import os
import struct 

class UdpClient:
	def __init__(self, server, port, buffersize, filename, cmd):
		self.server = server
		self.port = port
		self.buffersize = buffersize
		self.filename = filename
		self.cmd = cmd
		self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	def run(self):
		self.send_cmd()
		self.recieve_file()
		print("File %s saved" % self.filename)
		self.client_socket.close()

	def send(self): #send and wait for ack
		self.client_socket.sendto(self.data, (self.server, self.port))
		for i in range(3):
			try:
				ack = self.client_socket.recvfrom(self.buffersize)[0].decode()
				if ack == 'ACK':
					return
			except socket.timeout:
				pass
		print(self.error_msg, file=sys.stderr)
		sys.exit(1)

	def recv(self):
		self.data = (self.client_socket.recvfrom(self.buffersize))[0]
		self.client_socket.sendto("ACK".encode(), (self.server, self.port))


#send command to server
	def send_cmd(self):
		self.error_str = "Failed to send command. Terminating."
		# send length of command
		self.data = str(len(self.cmd)).encode()
		self.send()

		# send command
		self.data = self.cmd.encode()
		self.send()

#recieve packets from server
	def recieve_file(self):
		self.client_socket.settimeout(1)
		f = open(self.filename, 'wb')
		#recieve total length of file from server
		file_size = int(self.client_socket.recvfrom(self.buffersize)[0].decode())
		self.client_socket.sendto("ACK".encode(), (self.server, self.port))

		count = 0
		while count < file_size:
			# get chunk size
			self.recv()
			self.chunk_len = int(self.data.decode())
			count += self.chunk_len

			# get chunk and write to file
			self.recv()

			if len(self.data) != self.chunk_len:
				f.close()
				self.client_socket.close()
				print("Did not receive response.", file=sys.stderr)
				sys.exit(1)

			f.write(self.data)

		f.close()
		print("total file length: ", file_size)


if __name__ == '__main__':
	server = input("Enter server name or IP address: ")
	server = server.replace(" ", "")
	port = int(input("Enter port: "))
	if port < 0  or port > 65535:
		print("Invalid port number.", file=sys.stderr)
		sys.exit(1)

	cmd = input("Enter command: ")
	index = cmd.find('>')
	if index != -1:
		cmd_temp = cmd.split('>')
		cmd_temp = cmd_temp[len(cmd_temp)-1]
		cmd_temp = cmd_temp.replace(" ", "")
		filename = cmd_temp

	else: #client does not specify file name
		filename = 'udp_server_response.txt'

	Client = UdpClient(server, port, 512, filename, cmd)
	Client.run()


