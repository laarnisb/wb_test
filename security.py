from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import os

# Get the base64-encoded key from environment variable
key_b64 = os.getenv("ENCRYPTION_KEY")

# Decode it to get the 32-byte key
key = base64.urlsafe_b64decode(key_b64.encode())

def encrypt_data(data):
    try:
        cipher = AES.new(key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
        iv = base64.urlsafe_b64encode(cipher.iv).decode('utf-8')
        ct = base64.urlsafe_b64encode(ct_bytes).decode('utf-8')
        return iv + ":" + ct
    except Exception as e:
        return f"Encryption failed: {e}"

def decrypt_data(enc_data):
    try:
        iv_str, ct_str = enc_data.split(":")
        iv = base64.urlsafe_b64decode(iv_str.encode())
        ct = base64.urlsafe_b64decode(ct_str.encode())
        cipher = AES.new(key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        return pt.decode('utf-8')
    except Exception as e:
        return f"Decryption failed: {e}"
