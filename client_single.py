import socket
import sys

def http_client(server_host, server_port, filename):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        client_socket.connect((server_host, int(server_port))) 
        request_line = f"GET /{filename} HTTP/1.1\r\n" 
        headers = ( 
            f"Host: {server_host}:{server_port}\r\n"
            "Connection: close\r\n\r\n"
        )
        http_request = request_line + headers 
        client_socket.sendall(http_request.encode()) 
        response = b'' 
        while True:
            data = client_socket.recv(4096) 
            if not data: 
                break
            response += data 
        print("[RESPONSE FROM SERVER]:") 
        print(response.decode('utf-8', errors='replace'))

        client_socket.close() 

    except Exception as e:
        print(f"[ERROR]: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python client.py <server_host> <server_port> <filename>")
    else:
        _, host, port, file = sys.argv 
        http_client(host, port, file) 
