import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_addr = ('localhost', 8000)
print("Starting Server on port 8000")

sock.bind(server_addr)

sock.listen(1)

while True:
    print("Server Listening")
    connection, client_addr = sock.accept()

    try:
        print("Receive Connection from", client_addr)

        while True:
            data = connection.recv(16)
            print("Received {}".format(data))
            if not data:
                print("Data finished from {}".format(client_addr))
                break
    
    finally:
        connection.close()
