import socket
import threading
import os
import mimetypes
import time

def handle_client(conn, addr):
    try:
        req = conn.recv(1024).decode()
        print(f"[REQUEST from {addr}]:\n{req}")
        if not req:
            return
        time.sleep(5)
        path = req.split()[1].lstrip('/') or 'home.html'

        if os.path.isfile(path):
            with open(path, 'rb') as f:
                content = f.read()
            ctype = mimetypes.guess_type(path)[0] or 'application/octet-stream'
            headers = (
                f"HTTP/1.1 200 OK\r\n"
                f"Content-Type: {ctype}\r\n"
                f"Content-Length: {len(content)}\r\n"
                f"Connection: close\r\n\r\n"
            ).encode()
            conn.sendall(headers + content)
        else:
            resp = (
                "HTTP/1.1 404 Not Found\r\n"
                "Content-Type: text/html\r\n"
                "Connection: close\r\n\r\n"
                "<html><body><h1>404 Not Found</h1></body></html>"
            ).encode()
            conn.sendall(resp)
    except Exception as e:
        print(f"[ERROR]: {e}")
    finally:
        conn.close()

def start_server(port=2026):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(('', port))
        server.listen(10)
        print(f"[STARTING] Web Server running on port {port}...")

        try:
            while True:
                conn, addr = server.accept()
                threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
                print(f"[ACTIVE CONNECTIONS]: {threading.active_count() - 1}")
        except KeyboardInterrupt:
            print("\n[SHUTTING DOWN] Server stopped.")

if __name__ == "__main__":
    start_server()
