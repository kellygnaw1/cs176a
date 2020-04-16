import socket
import sys
import os

buffersize = 512

def recv(server_socket, error_msg):
	try:
		data, client_address = server_socket.recvfrom(buffersize)
		server_socket.sendto("ACK".encode(), client_address)
		return data.decode(), client_address
	except socket.timeout:
		print(error_msg, file=sys.stderr)
		sys.exit(1)

def send(server_socket, client_address, data, error_msg):
	server_socket.sendto(data, client_address)
	for i in range(3):
		try:
			ack = server_socket.recvfrom(buffersize)[0].decode()
			if(ack == 'ACK'):
				break
		except socket.timeout:
			pass

def receive_cmd(server_socket):

	error_str = "Failed to receive instructions from the client."

	# get command length
	cmd_len, client_address = recv(server_socket, error_str)
	cmd_len = int(cmd_len)

	# get command
	server_socket.settimeout(0.5)
	cmd = recv(server_socket, error_str)[0]
	assert(len(cmd) == cmd_len)
	return cmd, client_address


def create_file(cmd):
	index = cmd.find('>')
	if index != -1:
		cmd_temp = cmd.split('>')
		cmd_temp = cmd_temp[len(cmd_temp)-1]
		cmd_temp = cmd_temp.replace(" ", "")
		filename = cmd_temp
		os.system(cmd)
	else: # client does not specify file name
		filename = 'cmd.txt'
		os.system(cmd + ' > ' + filename)
	return filename


def send_file(server_socket, filename, client_address):
	server_socket.settimeout(1)

	# send file size
	f = open(filename, 'rb')
	file_size = os.stat(filename).st_size
	error_str = "File transmission failed."
	send(server_socket, client_address, str(file_size).encode(), error_str)

	# send file
	while True:
		read = f.read(buffersize)

		if not read:
			break

		# send length of data chunk
		send(server_socket, client_address, str(len(read)).encode(), error_str)

		# send data chunk
		send(server_socket, client_address, read, error_str)

	f.close()


def run():

	# create socket and bind
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind(('', int(sys.argv[1])))

	while True:
	# receive command
		cmd, client_address = receive_cmd(server_socket)
		filename = create_file(cmd)
		send_file(server_socket, filename, client_address)
		print("finished sending file to client")

if __name__ == '__main__':
	run()
