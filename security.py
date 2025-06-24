import os
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

key_b64 = os.getenv("ENCRYPTION_KEY")  # Should be 43-character base64 string
key = base64.urlsafe_b64decode(key_b64 + '==')  # Add padding back before decoding

def encrypt_message(message):
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted = cipher.encrypt(pad(message.encode(), AES.block_size))
    return base64.urlsafe_b64encode(encrypted).decode()

def decrypt_message(encrypted_message):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = unpad(cipher.decrypt(base64.urlsafe_b64decode(encrypted_message)), AES.block_size)
    return decrypted.decode()
