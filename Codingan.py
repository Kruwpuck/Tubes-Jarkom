import socket #Import module socket
import os   #Import module os

def handle_http_request(request): #Fungsi handle request dengan inputan request ouput return respone dari server
    method, path, _ = request.split('\n')[0].split() #Split pesan request kedalam 3 variable
    path = path[1:] #Menghilangkan tanda "/" pada file request dari client
    if path == "": #Pengecekan kondisi apakah file reqeust string kosong
        path = "index.html" #Jika True, ubah request file menjadi "index.html"
    if method == "GET": #Pengecekan kondisi jika method adalah GET
        if os.path.exists(path):    #Pengecekan kondisi jika file request berada pada server
            with open(path, 'rb') as file:  #Jika True, buka file
                file_content = file.read()  #Baca file dan masukan kedalam variable
            server_respone = "HTTP/1.1 200 OK\r\n"  #Membuat respone server OK
            response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(file_content)}\r\n\r\n".encode(
                'utf-8')    #Membuat respone server kemudia encode
            response += file_content    #menambahkan content yang diminta kedalam respone server
        else:   #Else
            server_respone = "HTTP/1.1 404 Not Found" #Membuat respon server jika file tidak ditemukan
            response = "HTTP/1.1 404 Not Found\r\n\r\nFile not found".encode('utf-8')   #Membuat respon server kemudian encode
        return server_respone, response #Retunr respon server
    else:   #Else jika method selain GET
        server_respone = "HTTP/1.1 405 Method Not Allowed"  #Membuat respone server bila methode bukan GET
        response = "HTTP/1.1 405 Method Not Allowed\r\n\r\nMethod not allowed".encode('utf-8')  #Membuat respone server kemudian encode
        return server_respone, response #Return server respone

def start_web_server(): #Main program
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #Buat socket TCP
    server_address = ('', 7999) #Inisiasi IP dan Port server
    server_socket.bind(server_address)  #Bind socket ke alamat dan port tertentu
    server_socket.listen(1) #Listen for incoming connections
    print('Web server telah dimulai di {}:{}'.format(server_address[0], server_address[1])) #Print server telah dimulai

    while True: #While True
        client_socket, client_address = server_socket.accept()  #Terima koneksi dari client
        print('Menerima koneksi dari: {}'.format(client_address))   #Cetak alamat client
        request = client_socket.recv(1024).decode('utf-8')  #Terima HTTP request dari client
        server_respone, response = handle_http_request(request) #Tangani HTTP request dan buat HTTP response
        method, req, protocol = request.split('\n')[0].split()  #Split request client ke dalam 3 variable
        filepath = os.path.join(os.getcwd(), request.split()[1][1:])    #Mencari filepath request file dari client
        print('Method   : {}'.format(method))   #Cetak method
        print('Request  : {}'.format(req))  #Cetak request
        print('Path     : {}'.format(filepath)) #Cetak filepath
        print('Protocol : {}'.format(protocol)) #Cetak protocol
        print('Respone  : {}\n'.format(server_respone)) #Cetak server respone
        client_socket.sendall(response) #Kirimkan HTTP response ke client
        client_socket.close()   #Tutup koneksi dengan client

if __name__ == '__main__': #Menjalankan main program
    start_web_server()
