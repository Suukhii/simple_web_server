#importing the nessessary modules
from socket import *
import sys 

#setting up the socket (TCP socket due to SOCK_STREAM)
serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 8000
serverIP = '127.0.0.1'


#Creates a connection from socket to server 
serverSocket.bind((serverIP, serverPort))
serverSocket.listen(1) 
print('Ready to serve...')


# Makes a server and tries to connect to 127.0.0.1/8000
while True:
    connectionSocket, addr = serverSocket.accept()
    print(f"Connection established with {addr}")
    
    try:
        message = connectionSocket.recv(1024).decode()
        if not message:
            connectionSocket.close()
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
            connectionSocket.send(header.encode())
            
            for line in outputdata:
                connectionSocket.send(line.encode())
        
        except IOError:
            print(f"File {filename} not found.")
            header = "HTTP/1.1 404 Not Found\r\n"
            header += "Content-Type: text/html\r\n"
            header += "Connection: close\r\n\r\n"
            connectionSocket.send(header.encode())  # Send header for 404
            connectionSocket.send("<html><body><h1>404 Not Found</h1></body></html>".encode())
        
        connectionSocket.close()

    except Exception as e:
        print(f"Error: {e}")
        connectionSocket.close()

serverSocket.close()
sys.exit()  