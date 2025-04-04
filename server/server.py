import socket
import threading
import os

HEADER = 64
PORT = 5051
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
FILENAME = "th.jpg"  


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(ADDR)

def send_file(conn):
    if not os.path.exists(FILENAME):
        print("[ERROR] File not found on server.")
        conn.send("0".encode(FORMAT))  
        return

    file_size = os.path.getsize(FILENAME)
    conn.send(f"{file_size:<{HEADER}}".encode(FORMAT))  

    with open(FILENAME, "rb") as f:
        while (chunk := f.read(1024)):  
            conn.send(chunk)

    print("[FILE SENT] File transfer complete.")

def handle_client(conn, addr):
   
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        try:
            msg_length = conn.recv(HEADER).decode(FORMAT).strip()
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)

                if msg == DISCONNECT_MESSAGE:
                    connected = False
                    print(f"[DISCONNECT] {addr} disconnected.")
                    break
                
                if msg == "SEND_FILE":
                    send_file(conn)
                else:
                    print(f"[{addr}] {msg}")
                    conn.send("Msg received".encode(FORMAT))

        except (ConnectionResetError, ValueError):
            print(f"[ERROR] Connection with {addr} lost.")
            connected = False

    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}:{PORT}")
    
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

print("[STARTING] Server is starting...")
start()
