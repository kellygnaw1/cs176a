import socket
import sys
import os

buffersize = 512
#add server response to file
def recieve_file(filename, client_socket):
	try:
		f = open(filename, "wb")

		while True:
			data = client_socket.recv(buffersize)
			if(len(data) < 1):
				return
			f.write(data)

		f.close()
		print("File %s saved" %filename)

	except Exception:
		client_socket.close()
		print("Did not recieve response", file=sys.stderr)
		sys.exit(1)

def run():
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	#request user server/port
	server = input("Enter server name or IP address: ")
	server = server.replace(" ", "")
	port = int(input("Enter port: "))
	if port < 0  or port > 65535:
	    print("Invalid port number.", file=sys.stderr)
	    sys.exit(1)
	#connect to server
	try:
		client_socket.connect((server, port))
	except socket.error:
		print("Could not connect to server.", file=sys.stderr)
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

	try:
		client_socket.send(cmd.encode())
	except Exception:
		client_socket.close()
		print("Did not recieve response", file=sys.stderr)
		sys.exit(1)

	recieve_file(filename, client_socket)
	print("File %s saved."%filename)
	client_socket.close()

if __name__ == '__main__':
	run()


