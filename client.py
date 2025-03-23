import argparse
from socket import *

def run_client(server_ip, server_port, file_name):
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((server_ip, server_port))

    request = f"GET {file_name} HTTP/1.1\r\nHost: {server_ip}\r\n\r\n"
    clientSocket.send(request.encode())

    response = clientSocket.recv(4096).decode()
    print("Server response:")
    print(response)

    clientSocket.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HTTP client to test the server")
    parser.add_argument("-i", "--server_ip", type=str, required=True, help="IP address of the server")
    parser.add_argument("-p", "--server_port", type=int, required=True, help="Port number on which the server is listening")
    parser.add_argument("-f", "--file", type=str, required=True, help="Path of the file to request from the server")

    args = parser.parse_args()

    run_client(args.server_ip, args.server_port, args.file)
