import base64
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Load and decode AES-256 key
raw_key = os.getenv("ENCRYPTION_KEY")
key = base64.b64decode(raw_key)  # Use standard b64decode

def encrypt_message(message):
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(message.encode(), AES.block_size))
    return base64.b64encode(cipher.iv + ct_bytes).decode()

def decrypt_message(ciphertext):
    data = base64.b64decode(ciphertext)
    iv = data[:AES.block_size]
    ct = data[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ct), AES.block_size).decode()
