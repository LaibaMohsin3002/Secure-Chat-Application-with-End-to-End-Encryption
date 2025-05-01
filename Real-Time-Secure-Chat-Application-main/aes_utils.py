# from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# from cryptography.hazmat.primitives import padding
# from cryptography.hazmat.backends import default_backend
# import base64
# import os

# # 16 bytes key (AES-128)
# def generate_key():
#     return os.urandom(16)

# def encrypt_aes(message, key):
#     iv = os.urandom(16)
#     cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())

#     padder = padding.PKCS7(128).padder()
#     padded_data = padder.update(message.encode()) + padder.finalize()

#     encryptor = cipher.encryptor()
#     ciphertext = encryptor.update(padded_data) + encryptor.finalize()

#     return base64.b64encode(iv + ciphertext).decode('utf-8')

# def decrypt_aes(ciphertext_b64, key):
#     ciphertext = base64.b64decode(ciphertext_b64.encode('utf-8'))
#     iv = ciphertext[:16]
#     ciphertext = ciphertext[16:]

#     cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
#     decryptor = cipher.decryptor()
#     padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

#     unpadder = padding.PKCS7(128).unpadder()
#     plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

#     return plaintext.decode('utf-8')
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import base64
import os
from cryptography.hazmat.primitives.ciphers import algorithms

# Shared DES key (must be 8 bytes for DES)
DES_KEY = b'8bytekey'  # Example: 8 bytes
DES_IV = b'8byteivv'   # DES block size is 8 bytes

# Shared AES key (16 bytes for AES-128)
AES_KEY = b'ThisIsASecretKey'  # 16-byte key, same for all clients and server
AES_IV = b'ThisIsAnInitVect'   # 16-byte IV, same for all clients and server

# You can generate a fixed key here or hardcode one as above.

def encrypt_aes(message):
    # Use the predefined AES key and IV for encryption
    iv = AES_IV  # Fixed IV
    cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(iv), backend=default_backend())

    # Padding to make message length a multiple of the block size (AES block size is 16)
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(message.encode()) + padder.finalize()

    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    # Return the base64 encoded string of IV + ciphertext
    return base64.b64encode(iv + ciphertext).decode('utf-8')

def decrypt_aes(ciphertext_b64):
    # Decode the base64 encoded ciphertext
    ciphertext = base64.b64decode(ciphertext_b64.encode('utf-8'))

    # Extract the IV and the actual ciphertext (first 16 bytes is IV)
    iv = ciphertext[:16]
    ciphertext = ciphertext[16:]

    # Decrypt using the same AES key and IV
    cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    # Remove padding
    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

    return plaintext.decode('utf-8')

def des_encrypt(message):
    cipher = Cipher(algorithms.DES(DES_KEY), modes.CBC(DES_IV), backend=default_backend())
    
    # Padding for DES (block size 8 bytes)
    padder = padding.PKCS7(64).padder()
    padded_data = padder.update(message.encode()) + padder.finalize()

    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    
    return base64.b64encode(DES_IV + ciphertext).decode('utf-8')

def des_decrypt(ciphertext_b64):
    ciphertext = base64.b64decode(ciphertext_b64.encode('utf-8'))
    
    iv = ciphertext[:8]
    ciphertext = ciphertext[8:]

    cipher = Cipher(algorithms.DES(DES_KEY), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    
    unpadder = padding.PKCS7(64).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
    
    return plaintext.decode('utf-8')
