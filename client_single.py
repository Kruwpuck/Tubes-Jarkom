import socket # Membuat socket client
import sys # Untuk menangani argumen baris perintah

def http_client(server_host, server_port, filename): 
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Membuat socket TCP
        client_socket.connect((server_host, int(server_port))) # Menghubungkan ke server
        request_line = f"GET /{filename} HTTP/1.1\r\n" # Membuat baris permintaan HTTP
        headers = ( 
            f"Host: {server_host}:{server_port}\r\n"
            "Connection: close\r\n\r\n"
        ) # Membuat header HTTP
        http_request = request_line + headers # Menggabungkan baris permintaan dan header
        client_socket.sendall(http_request.encode()) # Mengirim permintaan HTTP ke server
        response = b'' # Inisialisasi variabel untuk menyimpan respons
        while True: # Menerima respons dari server
            data = client_socket.recv(4096)  # Menerima data dari server
            if not data: # Jika tidak ada data yang diterima, keluar dari loop
                break
            response += data # Menambahkan data yang diterima ke respons
        print("[RESPONSE FROM SERVER]:") 
        print(response.decode('utf-8', errors='replace'))   # Mencetak respons dari server

        client_socket.close()  # Menutup koneksi socket

    except Exception as e: # Menangani kesalahan
        print(f"[ERROR]: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 4: # Memeriksa jumlah argumen yang diberikan
        print("Usage: python client.py <server_host> <server_port> <filename>")
    else:
        _, host, port, file = sys.argv  # Mengambil argumen dari baris perintah
        http_client(host, port, file) 
