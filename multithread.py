import threading
import requests

def request_page(i):
    try:
        response = requests.get('http://localhost:6789/home.html')
        print(f"[Thread-{i}] Status: {response.status_code}")
    except Exception as e:
        print(f"[Thread-{i}] Error: {e}")

threads = []

# Buat dan jalankan 10 thread
for i in range(10):
    t = threading.Thread(target=request_page, args=(i,))
    threads.append(t)
    t.start()

# Tunggu semua thread selesai
for t in threads:
    t.join()
