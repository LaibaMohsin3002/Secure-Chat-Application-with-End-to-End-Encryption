
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, filedialog, simpledialog
from cryptography.fernet import Fernet
import os
import subprocess
import platform

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 12345))

# Get encryption key
encryption_key = client.recv(1024)
cipher_suite = Fernet(encryption_key)

# GUI Setup
root = tk.Tk()
root.title("Secure Chat")
text_area = scrolledtext.ScrolledText(root)
text_area.pack(padx=10, pady=10)
text_area.config(state='disabled')

entry_field = tk.Entry(root)
entry_field.pack(padx=10, pady=(0,5), fill='x')

# Send button
send_button = tk.Button(root, text="Send Message", command=lambda: send_message())
send_button.pack(pady=(0, 10))

username = simpledialog.askstring("Username", "Enter your name:", parent=root)
client.send(cipher_suite.encrypt(username.encode()))

# Send text messages
def send_message():
    message = entry_field.get()
    if not message:
        return
    entry_field.delete(0, tk.END)
    text_area.config(state='normal')
    text_area.insert(tk.END, f"You: {message}\n")
    text_area.config(state='disabled')
    text_area.yview(tk.END)

    encrypted = cipher_suite.encrypt(message.encode())
    print(f"[ENCRYPTED] {encrypted}")
    client.send(encrypted)

entry_field.bind("<Return>", lambda e: send_message())

# Send files
def send_file():
    filepath = filedialog.askopenfilename()
    if not filepath:
        return
    filename = os.path.basename(filepath)
    with open(filepath, "rb") as f:
        data = f.read()
    encrypted_data = cipher_suite.encrypt(data)
    header = f"FILE:{filename}:{len(encrypted_data)}"
    client.send(cipher_suite.encrypt(header.encode()))
    client.send(encrypted_data)
    text_area.config(state='normal')
    text_area.insert(tk.END, f"You sent file: {filename}\n")
    text_area.config(state='disabled')
    text_area.yview(tk.END)

file_button = tk.Button(root, text="Send File", command=send_file)
file_button.pack(pady=(0,10))

# Platform-independent file opener
def open_file_callback(file_path):
    if platform.system() == 'Darwin':
        subprocess.call(('open', file_path))
    elif platform.system() == 'Windows':
        os.startfile(file_path)
    else:
        subprocess.call(('xdg-open', file_path))

# Add clickable file button
def add_file_button(display_name, path):
    btn = tk.Button(root, text=f"Open {display_name}", command=lambda: open_file_callback(path))
    btn.pack()

# Receive messages/files
def receive():
    while True:
        try:
            header = client.recv(1024)
            if not header:
                break
            decrypted_header = cipher_suite.decrypt(header).decode()
            if decrypted_header.startswith("FILE:"):
                _, filename, filesize = decrypted_header.split(":")
                filesize = int(filesize)
                encrypted_data = b""
                while len(encrypted_data) < filesize:
                    chunk = client.recv(min(4096, filesize - len(encrypted_data)))
                    encrypted_data += chunk
                data = cipher_suite.decrypt(encrypted_data)
                file_path = f"received_{filename}"
                with open(file_path, "wb") as f:
                    f.write(data)
                text_area.config(state='normal')
                text_area.insert(tk.END, f"File received: {filename}\n")
                text_area.config(state='disabled')
                text_area.yview(tk.END)
                add_file_button(filename, file_path)
            else:
                decrypted = decrypted_header
                print(f"[DECRYPTED] {decrypted}")
                text_area.config(state='normal')
                text_area.insert(tk.END, decrypted + "\n")
                text_area.config(state='disabled')
                text_area.yview(tk.END)
        except Exception as e:
            print("[ERROR]", e)
            break

threading.Thread(target=receive, daemon=True).start()

root.mainloop()
