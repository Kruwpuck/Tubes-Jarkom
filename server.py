import socket             # Mengimpor modul socket untuk komunikasi jaringan (TCP/IP).
import threading          # Mengimpor modul threading untuk menangani banyak klien secara bersamaan.
import os                 # Mengimpor modul os untuk operasi file (seperti cek apakah file ada).
import mimetypes          # Mengimpor modul mimetypes untuk menentukan tipe konten file (Content-Type).
import time               # Mengimpor modul time untuk menambahkan delay.

def handle_client(connection_socket, client_address): # Fungsi untuk menangani permintaan dari klien dalam 1 thead
    try:
        request = connection_socket.recv(1024).decode() # Menerima data dari klien (maksimal 1024 byte) dan mengubahnya ke string.
        print(f"[REQUEST from {client_address}]:\n{request}")  # Menampilkan permintaan dari klien di console.
        
        if not request: # Jika tidak ada permintaan yang diterima, tutup koneksi.
            return
        time.sleep(5) # Menambahkan delay 5 detik sebelum memproses permintaan .
        # Ekstrak filename dari request
        filename = request.split()[1].lstrip('/')  # Mengambil nama file dari permintaan HTTP (menghapus karakter '/' di depan).
        
        # Default file jika root
        if filename == '': # Misal http://localhost:6789/ maka akan muncul home.html sebagai default
            filename = 'home.html'
        
        # Cek apakah file ada
        if os.path.isfile(filename):
            with open(filename, 'rb') as file: # Membuka file dalam mode biner ('rb') untuk dibaca.
                content = file.read() # Membaca seluruh isi file.

            # Tentukan MIME type berdasarkan ekstensi file
            content_type = mimetypes.guess_type(filename)[0] or 'application/octet-stream' # Menentukan tipe konten file menggunakan modul mimetypes.

            # Header HTTP OK
            response_headers = ( 
                "HTTP/1.1 200 OK\r\n"
                f"Content-Type: {content_type}\r\n" 
                f"Content-Length: {len(content)}\r\n"
                "Connection: close\r\n\r\n"
            ).encode() # Mengubah header menjadi bytes, .encode bisa dibilang mengkodekan

            connection_socket.sendall(response_headers + content) # Mengirimkan header dan isi file ke klien.
        else: # Jika file tidak ditemukan
            # 404 Not Found
            response = (
                "HTTP/1.1 404 Not Found\r\n"
                "Content-Type: text/html\r\n"
                "Connection: close\r\n\r\n"
                "<html><body><h1>404 Not Found</h1></body></html>"
            ).encode()
            connection_socket.sendall(response) # Mengirimkan semua (sendall) respons 404 Not Found ke klien.

    except Exception as e: # Menangani kesalahan yang mungkin terjadi selama pemrosesan permintaan.
        print(f"[ERROR]: {e}")
    finally: # Menutup koneksi socket setelah selesai.
        connection_socket.close()


def start_server(server_port=6789): # Fungsi untuk memulai server HTTP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Membuat socket TCP/IP
    server_socket.bind(('', server_port)) # Mengikat socket ke alamat dan port yang ditentukan.
    server_socket.listen(5) # Mendengarkan koneksi masuk (maksimal 5 koneksi dalam antrean).
    print(f"[STARTING] Web Server running on port {server_port}...") 

    try:
        while True: # Loop utama server untuk menerima koneksi dari klien.
            client_socket, client_address = server_socket.accept() # Menerima koneksi dari klien.
            thread = threading.Thread(target=handle_client, args=(client_socket, client_address)) # Membuat thread baru untuk menangani klien.
            thread.start() # Memulai thread.
            print(f"[ACTIVE CONNECTIONS]: {threading.active_count() - 1}") # Menampilkan jumlah koneksi aktif (selain thread utama).
    except KeyboardInterrupt: # Menangani interupsi keyboard (Ctrl+C) untuk menghentikan server.
        print("\n[SHUTTING DOWN] Server stopped.") 
        server_socket.close()

if __name__ == "__main__":
    start_server()
