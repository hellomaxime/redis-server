from utils import deserialize, process, serialize
import socket
from _thread import start_new_thread

HOST = "127.0.0.1"
PORT = 6379

def new_client(conn, addr):
    with conn:
        print(f"Connection from {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            response = serialize(process(deserialize(data.decode())))
            conn.sendall(response.encode())

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        start_new_thread(new_client, (conn, addr))