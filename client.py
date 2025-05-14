import socket
import sys

def http_client(server_host, server_port, filename):
    try:
        # Buat socket dan koneksi ke server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Membuat socket TCP/IP
        client_socket.connect((server_host, int(server_port))) # Menghubungkan socket ke server dan port yang ditentukan.

        # Format permintaan GET
        request_line = f"GET /{filename} HTTP/1.1\r\n" # Membuat baris permintaan HTTP GET
        headers = ( 
            f"Host: {server_host}:{server_port}\r\n"
            "Connection: close\r\n\r\n"
        )
        http_request = request_line + headers # Menggabungkan baris permintaan dan header menjadi satu string

        # Kirim permintaan
        client_socket.sendall(http_request.encode()) # Mengirimkan permintaan ke server dalam bentuk bytes

        # Terima respons
        response = b'' # Inisialisasi variabel response sebagai bytes kosong
        while True:
            data = client_socket.recv(4096) # Menerima data dari server (maksimal 4096 byte)
            if not data: # Jika tidak ada data yang diterima, keluar dari loop
                break
            response += data # Menambahkan data yang diterima ke variabel response

        # Cetak response
        print("[RESPONSE FROM SERVER]:") 
        print(response.decode('utf-8', errors='replace')) # Mengubah bytes menjadi string dan menampilkan respons di console

        client_socket.close() # Menutup koneksi socket setelah selesai

    except Exception as e: # Menangani kesalahan yang mungkin terjadi selama pemrosesan permintaan.
        print(f"[ERROR]: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python client.py <server_host> <server_port> <filename>")
    else:
        _, host, port, file = sys.argv # Mengambil argumen dari command line, makanya pas manggil harus ada 3 argumen (ip, port dan file)
        http_client(host, port, file) 
