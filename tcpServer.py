 #!/ usr/bin/python
import socket, threading, sys

def banner():						#TODO:  Add functions.
	print "[***]	TCP Server p12		[***]"

bind_ip = sys.argv[1]
bind_port = sys.argv[2]
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)

print "[*] Listening on %s:%d" % (bind_ip, bind_port)

# client handling thread

def handle_client(client_socket):
    request = client_socket.recv(1024)
    print "[*] Received: %s" % request
    client_socket.send("ACK!")
    client_socket.close()
	while True:
	    client, addr = server.accept()
	    print "[*] Accepted connection from: %s:%d" % (addr[0], addr[1])
	    client_handler = threading.Thread(target=handle_client, args=(client,))
	    client_handler.start()

#TODO: ADD CODE BELOW INSIDE THE MAIN FUNCTION.  THIS WILL MAKE THE DEFAULT bind_ip 