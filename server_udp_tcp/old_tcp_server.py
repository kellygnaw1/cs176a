import socket
import sys
import os

buffersize = 512
def run():
	#establish tcp/ip with client
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	#socket address/port
	address = server_socket.bind(('', int(sys.argv[1])))

	#socket listen to one connection
	server_socket.listen(1)
	while True:
		conn, address = server_socket.accept()
		filename = create_file(conn)
		send_file(filename, conn)
		print("File transmission successful")

def recieve_cmd(conn):
	cmd = conn.recv(buffersize)
	if len(cmd) < 1:
		print("Failed to recieve instruction from the client.", file=sys.stderr)
		conn.close()
		sys.exit(1)
	return cmd.decode()

def create_file(conn):
	cmd = recieve_cmd(conn)
	index = cmd.find('>')
	if index != -1:
		cmd_temp = cmd.split('>')
		cmd_temp = cmd_temp[len(cmd_temp)-1]
		cmd_temp = cmd_temp.replace(" ", "")
		filename = cmd_temp
		os.system(cmd)

	else: #client does not specify file name
		filename = 'cmd.txt'
		os.system(cmd + '>' + filename)
	
	return filename

def send_file(filename, conn):
	f = open(filename, 'rb')

	try:
		while True:
			read = f.read(buffersize)

			if not read:
				break
			conn.sendall(read)
	except socket.error:
		print("File transmission failed.", file=sys.stderr)
		sys.exit(1)
	f.close()
	conn.close()

if __name__ == '__main__':
	run()







