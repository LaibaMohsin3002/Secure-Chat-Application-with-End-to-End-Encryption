import socket
import threading
from cryptography.fernet import Fernet

# Generate encryption key and cipher
encryption_key = Fernet.generate_key()
cipher_suite = Fernet(encryption_key)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 12345))
server.listen()

clients = {}
usernames = {}

# Helper: Broadcast to all clients except sender
def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                client.close()
                del clients[client]

# Handle incoming messages/files from clients
def handle_client(client_socket):
    try:
        username_encrypted = client_socket.recv(1024)
        username = cipher_suite.decrypt(username_encrypted).decode()
        usernames[client_socket] = username
        clients[client_socket] = username

        print(f"[JOINED] {username}")

        welcome_message = f"[Server] {username} joined the chat."
        encrypted_welcome = cipher_suite.encrypt(welcome_message.encode())
        broadcast(encrypted_welcome, client_socket)

        while True:
            header = client_socket.recv(1024)
            if not header:
                break

            header_decoded = cipher_suite.decrypt(header).decode()
            if header_decoded.startswith("FILE:"):
                _, filename, filesize = header_decoded.split(":")
                filesize = int(filesize)
                encrypted_data = b""
                while len(encrypted_data) < filesize:
                    chunk = client_socket.recv(min(4096, filesize - len(encrypted_data)))
                    encrypted_data += chunk

                print(f"[RECEIVED FILE] {filename} from {username} ({filesize} bytes)")

                # Broadcast file header
                for client in clients:
                    if client != client_socket:
                        client.send(cipher_suite.encrypt(f"FILE:{filename}:{filesize}".encode()))
                        client.send(encrypted_data)
            else:
                message = cipher_suite.decrypt(header).decode()
                full_message = f"{username}: {message}"
                print(f"[MSG] {full_message}")
                broadcast(cipher_suite.encrypt(full_message.encode()), client_socket)
    except:
        print(f"[DISCONNECTED] {usernames.get(client_socket, 'Unknown')}")
        client_socket.close()
        if client_socket in clients:
            del clients[client_socket]

print("[SERVER STARTED] Waiting for connections...")

while True:
    client_socket, addr = server.accept()
    print(f"[NEW CONNECTION] {addr}")
    client_socket.send(encryption_key)
    threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()
