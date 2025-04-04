import socket

HEADER = 64
PORT = 5051
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect(ADDR)
    print(f"[CONNECTED] Connected to server at {SERVER}:{PORT}")
except ConnectionRefusedError:
    print(f"[ERROR] Unable to connect to server at {SERVER}:{PORT}")
    exit()

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def receive_file(filename):
    print("[RECEIVING] Waiting for file size...")
    
    file_size_data = client.recv(HEADER).decode(FORMAT).strip()
    if not file_size_data.isdigit():
        print("[ERROR] Invalid file size received.")
        return
    
    file_size = int(file_size_data)
    print(f"[INFO] File size: {file_size} bytes")
    
    received_size = 0
    with open(filename, "wb") as f:
        while received_size < file_size:
            data = client.recv(min(1024, file_size - received_size))
            if not data:
                break
            f.write(data)
            received_size += len(data)
    
    print(f"[FILE RECEIVED] File saved as '{filename}'.")


send("SEND_FILE")
receive_file("received_client.jpg")

send("Hello Distributed System!")
input("Press Enter to send another message...")
send("Hello Everyone!")
input("Press Enter to send another message...")
send("Hello Sir Norman!")

send(DISCONNECT_MESSAGE)
client.close()
