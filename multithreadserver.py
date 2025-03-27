from socket import *
import sys
import threading

# Setting up the socket (TCP socket due to SOCK_STREAM)
server_socket = socket(AF_INET, SOCK_STREAM)
server_port = 8000
server_ip = '127.0.0.1'

# Bind the server to the IP and port
server_socket.bind((server_ip, server_port))
# Maximum of 5 clients can wait in the queue
server_socket.listen(5)  
print('Ready to serve...')

def handle_client(connection_socket, addr):
    """  
    Handles a client request by serving a requested file or returning a 404 error.

    Args:
        connectionSocket (socket): The client connection socket.
        addr (tuple): The client's address (IP, port).

    Workflow:
    - Reads the request and extracts the filename.
    - Sends the file if found; otherwise, returns a 404 response.
    - Closes the connection after handling the request.
    """
    
    
    print(f"Connection established with {addr}")
    try:
        message = connection_socket.recv(1024).decode()
        if not message:
            connection_socket.close()
            return
        
        print(f"Received message: {message}")
        
        filename = message.split()[1]
        if filename == '/':
            filename = '/index.html'
        
        print(f"Requested file: {filename}")

        try:
            with open(filename[1:], 'r') as file:
                outputdata = file.readlines()
            
            header = "HTTP/1.1 200 OK\r\n"
            header += "Content-Type: text/html\r\n"
            header += "Connection: close\r\n\r\n"
            connection_socket.send(header.encode())
            
            for line in outputdata:
                connection_socket.send(line.encode())
        
        except IOError:
            print(f"File {filename} not found.")
            header = "HTTP/1.1 404 Not Found\r\n"
            header += "Content-Type: text/html\r\n"
            header += "Connection: close\r\n\r\n"
            connection_socket.send(header.encode())  
            connection_socket.send("<html><body><h1>404 Not Found</h1></body></html>".encode())
    
    except Exception as e:
        print(f"Error: {e}")
    finally:
        connection_socket.close()

while True:
    connection_socket, addr = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(connection_socket, addr))
    client_thread.start()  
