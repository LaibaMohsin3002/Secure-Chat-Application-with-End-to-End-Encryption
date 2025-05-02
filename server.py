import socket #[1] Using sockets for TCP communication
import threading # [5] Multiplexing: Threads to handle multiple clients
import os
from cryptography.fernet import Fernet
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64


# [4] Admin selects encryption method - security at application layer (simulating app-layer service model)
method = input("Select encryption method (fernet/aes): ").strip().lower()
assert method in ["fernet", "aes"], "Invalid encryption method selected."


# [4] Setting up encryption - part of application layer
if method == "fernet":
    encryption_key = Fernet.generate_key()
    cipher_suite = Fernet(encryption_key)
else:
    encryption_key = get_random_bytes(32)
    iv = get_random_bytes(16)

    def aes_encrypt(data):
        cipher = AES.new(encryption_key, AES.MODE_CFB, iv=iv)
        return base64.b64encode(iv + cipher.encrypt(data))

    def aes_decrypt(data):
        raw = base64.b64decode(data)
        iv_in = raw[:16]
        cipher = AES.new(encryption_key, AES.MODE_CFB, iv=iv_in)
        return cipher.decrypt(raw[16:])


# [1] [3] [6] Creating TCP socket; congestion control and reliable transfer handled by TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
# server.bind(("localhost", 12345))
server.bind(("0.0.0.0", 12345))  # [1]
server.listen()  # [3] TCP connection wait (with implicit congestion control) [6]

clients = {}
usernames = {}

# Encryption helpers
def encrypt(data):
    return cipher_suite.encrypt(data) if method == "fernet" else aes_encrypt(data)

def decrypt(data):
    return cipher_suite.decrypt(data) if method == "fernet" else aes_decrypt(data)

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                client.close()
                del clients[client]

# [5] Threaded handler for client connection (multiplexing)
def handle_client(client_socket):
    try:
        username_encrypted = client_socket.recv(1024)
        username = decrypt(username_encrypted).decode()
        usernames[client_socket] = username
        clients[client_socket] = username

        print(f"[JOINED] {username}")
        welcome_message = f"[Server] {username} joined the chat."
        broadcast(encrypt(welcome_message.encode()), client_socket)

        while True:
            header = client_socket.recv(1024)
            if not header:
                break
            # Demultiplexing based on message type (text vs file)
            header_decoded = decrypt(header).decode()
            if header_decoded.startswith("FILE:"):
                _, filename, filesize = header_decoded.split(":")
                filesize = int(filesize)
                encrypted_data = b""
                while len(encrypted_data) < filesize:
                    chunk = client_socket.recv(min(4096, filesize - len(encrypted_data)))
                    encrypted_data += chunk

                print(f"[RECEIVED FILE] {filename} from {username} ({filesize} bytes)")

                for client in clients:
                    if client != client_socket:
                        client.send(encrypt(f"FILE:{filename}:{filesize}".encode()))
                        client.send(encrypted_data)
            else:
                # message = decrypt(header).decode()
                # print(f"[MSG] {username}: {message}")
                # broadcast(encrypt(f"{username}: {message}".encode()), client_socket)
                message = decrypt(header).decode().strip()
                if message.upper() == "QUIT":
                    print(f"[QUIT] {username} has left the chat.")
                    broadcast(encrypt(f"[Server] {username} has left the chat.".encode()), client_socket)
                    break
                print(f"[MSG] {username}: {message}")
                broadcast(encrypt(f"{username}: {message}".encode()), client_socket)

    except Exception as e:
        print(f"[DISCONNECTED] {usernames.get(client_socket, 'Unknown')} ({e})")
        client_socket.close()
        if client_socket in clients:
            del clients[client_socket]

print("[SERVER STARTED] Waiting for connections...")

while True:
    client_socket, addr = server.accept() # [3] Accepting TCP connection
    print(f"[NEW CONNECTION] {addr}")
    client_socket.send(method.encode())
    client_socket.send(encryption_key if method == "fernet" else base64.b64encode(encryption_key))
    threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()  #[5] Multiplexing: Threads to handle multiple clients

