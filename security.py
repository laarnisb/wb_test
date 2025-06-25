import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import streamlit as st

# Load and decode AES-256 key from Streamlit secrets
raw_key = st.secrets["ENCRYPTION_KEY"]
key = base64.b64decode(raw_key)  # Must decode to 32 bytes for AES-256

# Encrypt a message (e.g., before saving to DB)
def encrypt_message(message: str) -> str:
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(message.encode(), AES.block_size))
    return base64.b64encode(cipher.iv + ct_bytes).decode()

# Decrypt a message (e.g., after retrieving from DB)
def decrypt_message(ciphertext: str) -> str:
    data = base64.b64decode(ciphertext)
    iv = data[:AES.block_size]
    ct = data[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ct), AES.block_size).decode()
