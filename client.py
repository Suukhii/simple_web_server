import argparse
from socket import *

def run_client(server_ip, server_port, file_name):    
    """
    Simple HTTP Client
    
    This script acts as a basic HTTP client to send GET requests to a specified server 
    and retrieve responses. It connects to the server via a TCP socket, sends an HTTP 
    request for a specified file, and prints the server's response.

    Modules:
        - argparse: Parses command-line arguments.
        - socket: Handles network communication.

    Workflow:
        1. Establishes a TCP connection with the server.
        2. Sends an HTTP GET request for the specified file.
        3. Receives and displays the server's response.
        4. Closes the connection.

    """
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    request = f"GET {file_name} HTTP/1.1\r\nHost: {server_ip}\r\n\r\n"
    client_socket.send(request.encode())

    response = client_socket.recv(4096).decode()
    print("Server response:")
    print(response)

    client_socket.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HTTP client to test the server")
    parser.add_argument("-i", "--server_ip", type=str, required=True, help="IP address of the server")
    parser.add_argument("-p", "--server_port", type=int, required=True, help="Port number on which the server is listening")
    parser.add_argument("-f", "--file", type=str, required=True, help="Path of the file to request from the server")

    args = parser.parse_args()

    run_client(args.server_ip, args.server_port, args.file)
