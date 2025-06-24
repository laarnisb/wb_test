from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import streamlit as st

# Load the 256-bit key (Base64-encoded)
key = base64.urlsafe_b64decode(st.secrets["ENCRYPTION_KEY"])

BLOCK_SIZE = 16  # AES block size

def encrypt_message(message: str) -> str:
    """Encrypts a message using AES-256-CBC."""
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(message.encode(), BLOCK_SIZE))
    iv = base64.urlsafe_b64encode(cipher.iv).decode()
    ct = base64.urlsafe_b64encode(ct_bytes).decode()
    return f"{iv}:{ct}"

def decrypt_message(encrypted_message: str) -> str:
    """Decrypts an AES-256-CBC message."""
    try:
        iv_b64, ct_b64 = encrypted_message.split(":")
        iv = base64.urlsafe_b64decode(iv_b64)
        ct = base64.urlsafe_b64decode(ct_b64)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct), BLOCK_SIZE)
        return pt.decode()
    except Exception as e:
        return f"Decryption failed: {str(e)}"
