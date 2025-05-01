import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, filedialog, simpledialog
from cryptography.fernet import Fernet
from Crypto.Cipher import AES
import os
import base64
import platform
import subprocess

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect(("localhost", 12345))

server_ip = simpledialog.askstring("Server IP", "Enter server IP:", parent=None)
client.connect((server_ip, 12345))

method = client.recv(1024).decode().strip().lower()
key = client.recv(1024)

if method == "fernet":
    cipher_suite = Fernet(key)
    print(f"[FERNET] Key: {key.decode()}")
else:
    encryption_key = base64.b64decode(key)
    print(f"[AES] Key: {base64.b64encode(encryption_key).decode()}")

    def aes_encrypt(data):
        iv = os.urandom(16)
        cipher = AES.new(encryption_key, AES.MODE_CFB, iv=iv)
        encrypted = cipher.encrypt(data)
        result = base64.b64encode(iv + encrypted)
        print(f"[AES ENCRYPT] Raw: {data}, Encrypted: {result}")
        return result

    def aes_decrypt(data):
        raw = base64.b64decode(data)
        iv_in = raw[:16]
        cipher = AES.new(encryption_key, AES.MODE_CFB, iv=iv_in)
        decrypted = cipher.decrypt(raw[16:])
        print(f"[AES DECRYPT] Raw: {data}, Decrypted: {decrypted}")
        return decrypted

def encrypt(data):
    if method == "fernet":
        encrypted = cipher_suite.encrypt(data)
        print(f"[FERNET ENCRYPT] {data} → {encrypted}")
        return encrypted
    return aes_encrypt(data)

def decrypt(data):
    if method == "fernet":
        decrypted = cipher_suite.decrypt(data)
        print(f"[FERNET DECRYPT] {data} → {decrypted}")
        return decrypted
    return aes_decrypt(data)

root = tk.Tk()
root.title("Secure Chat")
text_area = scrolledtext.ScrolledText(root)
text_area.pack(padx=10, pady=10)
text_area.config(state='disabled')

entry_field = tk.Entry(root)
entry_field.pack(padx=10, pady=(0,5), fill='x')
send_button = tk.Button(root, text="Send Message", command=lambda: send_message())
send_button.pack(pady=(0, 10))

username = simpledialog.askstring("Username", "Enter your name:", parent=root)
client.send(encrypt(username.encode()))

def send_message():
    message = entry_field.get()
    if not message:
        return
    entry_field.delete(0, tk.END)
    text_area.config(state='normal')
    text_area.insert(tk.END, f"You: {message}\n")
    text_area.config(state='disabled')
    text_area.yview(tk.END)
    encrypted = encrypt(message.encode())
    print(f"[SEND] Sending: {message} → {encrypted}")
    client.send(encrypted)

entry_field.bind("<Return>", lambda e: send_message())

def send_file():
    filepath = filedialog.askopenfilename()
    if not filepath:
        return
    filename = os.path.basename(filepath)
    with open(filepath, "rb") as f:
        data = f.read()
    encrypted_data = encrypt(data)
    header = f"FILE:{filename}:{len(encrypted_data)}"
    client.send(encrypt(header.encode()))
    client.send(encrypted_data)
    print(f"[SEND FILE] Sent {filename} ({len(encrypted_data)} bytes)")
    text_area.config(state='normal')
    text_area.insert(tk.END, f"You sent file: {filename}\n")
    text_area.config(state='disabled')
    text_area.yview(tk.END)

file_button = tk.Button(root, text="Send File", command=send_file)
file_button.pack(pady=(0,10))

def open_file_callback(file_path):
    if platform.system() == 'Darwin':
        subprocess.call(('open', file_path))
    elif platform.system() == 'Windows':
        os.startfile(file_path)
    else:
        subprocess.call(('xdg-open', file_path))

def add_file_button(display_name, path):
    btn = tk.Button(root, text=f"Open {display_name}", command=lambda: open_file_callback(path))
    btn.pack()

def quit_chat():
    client.send(encrypt("QUIT".encode()))
    root.destroy()
    client.close()

quit_button = tk.Button(root, text="Quit", command=quit_chat)
quit_button.pack(pady=(0,10))

def receive():
    while True:
        try:
            header = client.recv(1024)
            if not header:
                break
            decrypted_header = decrypt(header).decode()
            print(f"[RECEIVED] Header Decrypted: {decrypted_header}")
            if decrypted_header.startswith("FILE:"):
                _, filename, filesize = decrypted_header.split(":")
                filesize = int(filesize)
                encrypted_data = b""
                while len(encrypted_data) < filesize:
                    chunk = client.recv(min(4096, filesize - len(encrypted_data)))
                    encrypted_data += chunk
                data = decrypt(encrypted_data)
                file_path = f"received_{filename}"
                with open(file_path, "wb") as f:
                    f.write(data)
                print(f"[RECEIVED FILE] Saved as {file_path}")
                text_area.config(state='normal')
                text_area.insert(tk.END, f"File received: {filename}\n")
                text_area.config(state='disabled')
                text_area.yview(tk.END)
                add_file_button(filename, file_path)
            else:
                decrypted = decrypted_header
                text_area.config(state='normal')
                text_area.insert(tk.END, decrypted + "\n")
                text_area.config(state='disabled')
                text_area.yview(tk.END)
        except Exception as e:
            print("[ERROR]", e)
            break

threading.Thread(target=receive, daemon=True).start()
root.mainloop()
