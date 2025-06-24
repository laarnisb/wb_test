from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import os
import streamlit as st

# Load the encryption key from Streamlit secrets
ENCRYPTION_KEY = base64.urlsafe_b64decode(st.secrets["ENCRYPTION_KEY"])

def encrypt_message(message):
    cipher = AES.new(ENCRYPTION_KEY, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(message.encode(), AES.block_size))
    iv = base64.urlsafe_b64encode(cipher.iv).decode()
    ct = base64.urlsafe_b64encode(ct_bytes).decode()
    return f"{iv}:{ct}"

def decrypt_message(encrypted):
    try:
        iv, ct = encrypted.split(":")
        iv = base64.urlsafe_b64decode(iv)
        ct = base64.urlsafe_b64decode(ct)
        cipher = AES.new(ENCRYPTION_KEY, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size).decode()
        return pt
    except Exception as e:
        return f"Decryption failed: {str(e)}"
