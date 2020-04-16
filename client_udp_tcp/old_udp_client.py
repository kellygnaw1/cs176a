import socket
import sys
import os
import struct 

buffersize = 512

def send(data, client_socket, server, port, error_msg):
	client_socket.sendto(data, (server, port))
	for i in range(3):
		try:
			ack = client_socket.recvfrom(buffersize)[0].decode()
			if ack == 'ACK':
				return
		except socket.timeout:
			pass
	print(error_msg, file=sys.stderr)
	sys.exit(1)

def recv(client_socket, server, port):
	data = (client_socket.recvfrom(buffersize))[0]
	client_socket.sendto("ACK".encode(), (server, port))
	return data

#send command to server
def send_cmd(client_socket, server, port, cmd):
	error_str = "Failed to send command. Terminating."
	# send length of command
	send(str(len(cmd)).encode(), client_socket, server, port, error_str)

	# send command
	send(cmd.encode(), client_socket, server, port, error_str)

#recieve packets from server
def recieve_file(client_socket, server, port, filename):

	f = open(filename, 'wb')

	file_size = int(client_socket.recvfrom(buffersize)[0].decode())
	client_socket.sendto("ACK".encode(), (server, port))

	count = 0
	while count < file_size:
		# get chunk size
		chunk_len = int(recv(client_socket, server, port).decode())
		count += chunk_len

		# get chunk and write to file
		data = recv(client_socket, server, port)
		if len(data) != chunk_len:
			f.close()
			client_socket.close()
			print("Did not receive response.", file=sys.stderr)
			sys.exit(1)

		f.write(data)

	f.close()
	print("total file length: ", file_size)

def run():

	# create socket
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	client_socket.settimeout(1)

	# get configuration
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

	send_cmd(client_socket, server, port, cmd)
	recieve_file(client_socket, server, port, filename)
	print("File %s saved" % filename)
	client_socket.close()

if __name__ == '__main__':

	run()