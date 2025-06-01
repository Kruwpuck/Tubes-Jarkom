import threading
import socket
import sys

def request_page(i, host, port, file):
    try:
        s = socket.create_connection((host, int(port)))
        request = f"GET /{file} HTTP/1.1\r\nHost: {host}:{port}\r\nConnection: close\r\n\r\n"
        s.sendall(request.encode())

        response = b""
        while True:
            data = s.recv(4096)
            if not data:
                break
            response += data

        s.close()
        print(f"[Thread-{i} RESPONSE FROM SERVER]:")
        print(response.decode('utf-8', errors='replace'))
        print() 

    except Exception as e:
        print(f"[Thread-{i} ERROR]: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <server_host> <server_port> <filename>")
        sys.exit(1)

    _, host, port, file = sys.argv

    threads = [threading.Thread(target=request_page, args=(i, host, port, file)) for i in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
