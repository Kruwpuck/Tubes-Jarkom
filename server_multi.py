import socket # Membuat socket server
import threading # Untuk menangani beberapa koneksi klien secara bersamaan
import os # Mencari file yang diminta
import mimetypes # Menentukan tipe konten file
import time # Untuk simulasi delay

def handle_client(conn, addr): # Menangani koneksi klien
    try:
        req = conn.recv(1024).decode() # Menerima permintaan dari klien
        print(f"[REQUEST from {addr}]:\n{req}") # Mencetak permintaan klien
        if not req: # Jika tidak ada permintaan, keluar dari fungsi
            return
        time.sleep(5) # Simulasi delay 5 detik
        path = req.split()[1].lstrip('/') or 'home.html' # Mengambil path dari permintaan, default ke 'home.html'

        if os.path.isfile(path): # Memeriksa apakah file ada
            with open(path, 'rb') as f: # Membuka file dalam mode baca biner
                content = f.read() # Membaca konten file
            ctype = mimetypes.guess_type(path)[0] or 'application/octet-stream' # Menentukan tipe konten file
            headers = (
                f"HTTP/1.1 200 OK\r\n"
                f"Content-Type: {ctype}\r\n"
                f"Content-Length: {len(content)}\r\n"
                f"Connection: close\r\n\r\n"
            ).encode() # Membuat header HTTP
            conn.sendall(headers + content) # Mengirim header dan konten file ke klien
        else:
            resp = (
                "HTTP/1.1 404 Not Found\r\n"
                "Content-Type: text/html\r\n"
                "Connection: close\r\n\r\n"
                "<html><body><h1>404 Not Found</h1></body></html>"
            ).encode() # Jika file tidak ditemukan, mengirimkan respons 404
            conn.sendall(resp) # Mengirimkan respons 404 ke klien
    except Exception as e: # Menangani kesalahan
        print(f"[ERROR]: {e}") # Mencetak pesan kesalahan
    finally:
        conn.close() # Menutup koneksi klien

def start_server(port=2026): # Memulai server pada port yang ditentukan
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server: # Membuat socket TCP
        server.bind(('', port)) # Mengikat socket ke alamat dan port
        server.listen(10) # Mendengarkan koneksi masuk
        print(f"[STARTING] Web Server running on port {port}...") 

        try:
            while True: 
                conn, addr = server.accept() # Menerima koneksi dari klien
                threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start() # Menangani koneksi klien dalam thread terpisah
                print(f"[ACTIVE CONNECTIONS]: {threading.active_count() - 1}") 
        except KeyboardInterrupt: # Menangani interupsi keyboard (Ctrl+C)
            print("\n[SHUTTING DOWN] Server stopped.")

if __name__ == "__main__":
    start_server()
