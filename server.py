"""
Simple HTTP Server

This script creates a basic HTTP server that listens on 127.0.0.1:8000 and serves HTML files 
to clients over a TCP connection. It handles HTTP GET requests and responds with the requested 
file's contents if available; otherwise, it returns a 404 Not Found error.

Workflow:
    1. Sets up a TCP server socket and binds it to IP 127.0.0.1 on port 8000.
    2. Listens for incoming client connections.
    3. Handles requests:
        - Reads the HTTP request from the client.
        - Extracts the requested file name.
        - If the file exists, sends an HTTP 200 response with the file content.
        - If the file is missing, responds with a 404 error.
    4. Closes the client connection after handling the reques

"""

from socket import *
import sys 

#setting up the socket (TCP socket due to SOCK_STREAM)
server_socket = socket(AF_INET, SOCK_STREAM)
server_port = 8000
server_ip = '127.0.0.1'


#Creates a connection from socket to server 
server_socket.bind((server_ip, server_port))
server_socket.listen(1) 
print('Ready to serve...')


# Makes a server and tries to connect to 127.0.0.1/8000
while True:
    connection_socket, addr = server_socket.accept()
    print(f"Connection established with {addr}")
    
    try:
        message = connection_socket.recv(1024).decode()
        if not message:
            connection_socket.close()
            continue
        
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
            connection_socket.send(header.encode())  # Send header for 404
            connection_socket.send("<html><body><h1>404 Not Found</h1></body></html>".encode())
        
        connection_socket.close()

    except Exception as e:
        print(f"Error: {e}")
        connection_socket.close()

server_socket.close()
sys.exit()  