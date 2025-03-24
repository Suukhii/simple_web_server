from socket import *
import sys
import threading

# Setting up the socket (TCP socket due to SOCK_STREAM)
serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 8000
serverIP = '127.0.0.1'

# Bind the server to the IP and port
serverSocket.bind((serverIP, serverPort))
serverSocket.listen(5)  # Maximum of 5 clients can wait in the queue
print('Ready to serve...')

def handle_client(connectionSocket, addr):
    """ Function to handle each client request in a separate thread """
    print(f"Connection established with {addr}")
    try:
        message = connectionSocket.recv(1024).decode()
        if not message:
            connectionSocket.close()
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
    
    except Exception as e:
        print(f"Error: {e}")
    finally:
        connectionSocket.close()

# Server loop that listens for incoming connections and starts a new thread for each client
while True:
    connectionSocket, addr = serverSocket.accept()
    # Create a new thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(connectionSocket, addr))
    client_thread.start()  # Start the thread
