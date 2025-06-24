import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

import os

# Load key from Streamlit secrets and decode
raw_key = os.getenv("ENCRYPTION_KEY")  # base64-encoded string
key = base64.urlsafe_b64decode(raw_key)  # convert to 32-byte key

def encrypt_message(message):
    cipher = AES.new(key, AES.MODE_ECB)
    ct_bytes = cipher.encrypt(pad(message.encode(), AES.block_size))
    return base64.urlsafe_b64encode(ct_bytes).decode()

def decrypt_message(encrypted):
    cipher = AES.new(key, AES.MODE_ECB)
    pt = unpad(cipher.decrypt(base64.urlsafe_b64decode(encrypted)), AES.block_size)
    return pt.decode()
