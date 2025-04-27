# # # Import required modules
# # import socket
# # import threading
# # import secrets
# # from tkinter import E
# # import el_gamal
# # import RSA

# # HOST = '192.168.1.8'
# # #HOST = '192.168.116.112'
# # PORT = 1234 # to 65535
# # LISTENER_LIMIT = 5
# # active_clients = [] # List of all currently connected users

    
# # #Function to choose which security method to use
# # def chooseMethod():
# #     lst = ["DES","ELGAMAL","RSA"]
# #     print("---------Welcome to our secure chat")
# #     print("1- DES (Data encryption standard)")
# #     print("2- ElGamal encryption system")
# #     print("3- RSA (Rivest–Shamir–Adleman)")
# #     num = input("Choose the encryption system: ")
# #     print(lst[int(num)-1] + " mode has been started")
# #     return num

# # def getMethod():
# #     return flagmethod
   
# # # Function to listen for upcoming messages from a client
# # def listen_for_messages(client, username,key,elgamapublickey,rsa_string):

# #     while 1:

# #         message = client.recv(2048).decode('utf-8')
# #         print("RECV : ",message)
# #         if message != '':
# #             ####### send
# #             final_msg = username + '~' + message + '~' + key + "~" +flagmethod+"~"+elgamapublickey+"~"+rsa_string
# #             send_messages_to_all(final_msg)
# #             print("rsaaaaaaa:   ",final_msg)

# #         else:
# #             print(f"The message send from client {username} is empty")


# # # Function to send message to a single client
# # def send_message_to_client(client, message):

# #     client.sendall(message.encode())
# #     print("SEND : ", message.encode() )

# # # Function to send any new message to all the clients that
# # # are currently connected to this server
# #     #####here
# # def send_messages_to_all(message):
    
# #     for user in active_clients:
        
# #         # Start the security phase using message then pass the message to client
# #         send_message_to_client(user[1], message)

# # # Function to handle client
# # def client_handler(client,key):
    
# #     # Server will listen for client message that will
# #     # Contain the username
# #     while 1:

# #         username = client.recv(2048).decode('utf-8')
# #         print("RECV : ",username)
# #         if username != '':
# #             active_clients.append((username, client,key))
# #             # generate session key
# #             key = secrets.token_hex(8).upper()
# #             ### RSA parameters ###
# #             #key of RSA Parameters 
# #             n,E,D=RSA.calc() 
# #             print("public and private key paramters: ")
# #             print("n: ",n)
# #             print("E: ",E)
# #             print("D: ",D)
# #             print("")
# #             print("")
            
# #             rsa_string=""

# #             rsa_string+=str(n)
# #             rsa_string+=","            
# #             rsa_string+=str(E)
# #             rsa_string+=","
# #             rsa_string+=str(D)
# #             rsa_string+=","

            


# #             string_ints = [str(x) for x in ElgamalKey]
# #             elgamalpublickey = ",".join(string_ints)
# #             print("elgamal public key",elgamalpublickey)





# #             #########send
# #             prompt_message = "SERVER~" + f"{username} added to the chat~" + key + "~" +flagmethod +"~" + elgamalpublickey +"~"+rsa_string 
# #             send_messages_to_all(prompt_message)
            
# #             print("Sessison key successfully generated for " + f"{username } ==>",key)

# #             break
# #         else:
# #             print("Client username is empty")

# #     threading.Thread(target=listen_for_messages, args=(client, username, key,elgamalpublickey,rsa_string, )).start()


# # # Main function
# # def main():
# #     global ElgamalKey
# #     ElgamalKey = el_gamal.generate_public_key()
# #     # Creating the socket class object
# #     # AF_INET: we are going to use IPv4 addresses
# #     # SOCK_STREAM: we are using TCP packets for communication
# #     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
# #     #choose method
# #     global flagmethod
# #     flagmethod = chooseMethod()
    
# #     # Creating a try catch block
# #     try:
# #         server.bind((HOST, PORT))
# #         print(f"Running the server on {HOST} {PORT}")
# #     except:
# #         print(f"Unable to bind to host {HOST} and port {PORT}")
    
    
# #     # Set server limit
# #     server.listen(LISTENER_LIMIT)

# #     # This while loop will keep listening to client connections
# #     while 1:

# #         client, address = server.accept()
# #         print(f"Successfully connected to client {address[0]} {address[1]}")
# #         key = ""
# #         threading.Thread(target=client_handler, args=(client,key, )).start()


# # if __name__ == '__main__':
# #     main()


# # Import required modules
# import socket
# import threading
# import secrets
# import el_gamal
# import RSA

# # HOST = '192.168.1.8'
# # PORT = 1234
# HOST = '127.0.0.1'  # Localhost
# PORT = 1234         # Or any port above 1024 that's not in use
# LISTENER_LIMIT = 5
# active_clients = []


# # Placeholder encryption functions
# def des_encrypt(msg, key):
#     return f"[DES_ENCRYPTED]{msg}"

# def elgamal_encrypt(msg, public_key):
#     return f"[ELGAMAL_ENCRYPTED]{msg}"

# def rsa_encrypt(msg, n, e):
#     return f"[RSA_ENCRYPTED]{msg}"

# # Function to choose which security method to use
# def chooseMethod():
#     lst = ["DES", "ELGAMAL", "RSA"]
#     print("---------Welcome to our secure chat---------")
#     print("1 - DES (Data Encryption Standard)")
#     print("2 - ElGamal Encryption System")
#     print("3 - RSA (Rivest–Shamir–Adleman)")
#     num = input("Choose the encryption system: ")
#     print(lst[int(num)-1] + " mode has been started\n")
#     return num

# # Function to listen for incoming messages from a client
# def listen_for_messages(client, username, key, elgamapublickey, rsa_string):
#     global flagmethod
#     rsa_parts = rsa_string.split(",")
#     rsa_n = int(rsa_parts[0])
#     rsa_e = int(rsa_parts[1])

#     while True:
#         message = client.recv(2048).decode('utf-8')
#         print("RECV :", message)
#         if message != '':
#             # Encrypt message based on selected method
#             if flagmethod == "1":
#                 encrypted_msg = des_encrypt(message, key)
#             elif flagmethod == "2":
#                 encrypted_msg = elgamal_encrypt(message, elgamapublickey)
#             elif flagmethod == "3":
#                 encrypted_msg = rsa_encrypt(message, rsa_n, rsa_e)
#             else:
#                 encrypted_msg = message  # fallback

#             final_msg = username + '~' + encrypted_msg + '~' + key + "~" + flagmethod + "~" + elgamapublickey + "~" + rsa_string
#             send_messages_to_all(final_msg)
#         else:
#             print(f"The message sent from client {username} is empty")

# # Function to send message to a single client
# def send_message_to_client(client, message):
#     client.sendall(message.encode())
#     print("SEND :", message.encode())

# # Function to broadcast message to all connected clients
# def send_messages_to_all(message):
#     for user in active_clients:
#         send_message_to_client(user[1], message)

# # Function to handle individual client connection
# def client_handler(client, key):
#     global flagmethod

#     while True:
#         username = client.recv(2048).decode('utf-8')
#         print("RECV :", username)
#         if username != '':
#             active_clients.append((username, client, key))

#             # Generate session key
#             key = secrets.token_hex(8).upper()

#             # RSA key generation
#             n, E, D = RSA.calc()
#             rsa_string = f"{n},{E},{D},"

#             # ElGamal public key
#             string_ints = [str(x) for x in ElgamalKey]
#             elgamalpublickey = ",".join(string_ints)
#             print("elgamal public key", elgamalpublickey)

#             # Notify others
#             prompt_message = "SERVER~" + f"{username} added to the chat~" + key + "~" + flagmethod + "~" + elgamalpublickey + "~" + rsa_string
#             send_messages_to_all(prompt_message)
#             print("Session key generated for", username, "==>", key)
#             break
#         else:
#             print("Client username is empty")

#     threading.Thread(target=listen_for_messages, args=(client, username, key, elgamalpublickey, rsa_string)).start()

# # Main function to start the server
# def main():
#     global ElgamalKey
#     global flagmethod

#     ElgamalKey = el_gamal.generate_public_key()
#     flagmethod = chooseMethod()

#     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#     try:
#         server.bind((HOST, PORT))
#         print(f"Running the server on {HOST}:{PORT}")
#     except:
#         print(f"Unable to bind to host {HOST} and port {PORT}")
#         return

#     server.listen(LISTENER_LIMIT)
#     print("Server is listening for connections...\n")

#     while True:
#         client, address = server.accept()
#         print(f"Connected to client {address[0]}:{address[1]}")
#         key = ""
#         threading.Thread(target=client_handler, args=(client, key)).start()

# if __name__ == '__main__':
#     main()

import socket
import threading
import secrets
import el_gamal
import RSA

HOST = '127.0.0.1'
PORT = 1234
LISTENER_LIMIT = 5
active_clients = []

def chooseMethod():
    print("---------Welcome to our secure chat---------")
    print("1 - DES (Data Encryption Standard)")
    print("2 - ElGamal Encryption System")
    print("3 - RSA (Rivest-Shamir-Adleman)")
    while True:
        num = input("Choose the encryption system (1-3): ")
        if num in ['1', '2', '3']:
            methods = ["DES", "ELGAMAL", "RSA"]
            print(f"{methods[int(num)-1]} mode has been started\n")
            return num
        print("Invalid choice. Please enter 1, 2, or 3.")

def client_handler(client, key):
    global flagmethod
    
    while True:
        username = client.recv(2048).decode('utf-8')
        if username:
            # Generate session key for DES
            key = secrets.token_hex(8).upper()
            
            # Generate RSA keys
            n, E, D = RSA.calc()
            rsa_string = f"{n},{E},{D}"
            
            # Get ElGamal public key
            elgamal_key = el_gamal.generate_public_key()
            elgamalpublickey = ",".join(map(str, elgamal_key))
            
            active_clients.append((username, client, key))
            
            prompt_message = f"SERVER~{username} joined the chat~{key}~{flagmethod}~{elgamalpublickey}~{rsa_string}"
            send_messages_to_all(prompt_message)
            
            threading.Thread(target=listen_for_messages, 
                          args=(client, username, key, elgamalpublickey, rsa_string)).start()
            break

def listen_for_messages(client, username, key, elgamalpublickey, rsa_string):
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
            if message:
                final_msg = f"{username}~{message}~{key}~{flagmethod}~{elgamalpublickey}~{rsa_string}"
                send_messages_to_all(final_msg)
        except:
            remove_client(client)
            break

def send_message_to_client(client, message):
    try:
        client.sendall(message.encode())
    except:
        remove_client(client)

def send_messages_to_all(message):
    for user in active_clients:
        send_message_to_client(user[1], message)

def remove_client(client):
    for i, user in enumerate(active_clients):
        if user[1] == client:
            del active_clients[i]
            break

def main():
    global flagmethod
    flagmethod = chooseMethod()
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((HOST, PORT))
        print(f"Server running on {HOST}:{PORT}")
    except:
        print(f"Failed to bind to {HOST}:{PORT}")
        return

    server.listen(LISTENER_LIMIT)
    print("Waiting for connections...\n")

    while True:
        client, address = server.accept()
        print(f"Connected to {address[0]}:{address[1]}")
        threading.Thread(target=client_handler, args=(client, "")).start()

if __name__ == '__main__':
    main()