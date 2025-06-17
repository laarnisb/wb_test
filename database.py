import os
import psycopg2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

# Load encryption key from Streamlit secrets or environment
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", "missing_key").encode()
BLOCK_SIZE = 16

def encrypt_data(data):
    cipher = AES.new(ENCRYPTION_KEY, AES.MODE_ECB)
    encrypted = cipher.encrypt(pad(data.encode(), BLOCK_SIZE))
    return base64.b64encode(encrypted).decode()

def decrypt_data(encrypted_data):
    cipher = AES.new(ENCRYPTION_KEY, AES.MODE_ECB)
    decrypted = unpad(cipher.decrypt(base64.b64decode(encrypted_data)), BLOCK_SIZE)
    return decrypted.decode()

def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

def insert_transaction(user_id, amount, category, description):
    enc_description = encrypt_data(description)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO transactions (user_id, amount, category, description)
        VALUES (%s, %s, %s, %s)
    """, (user_id, amount, category, enc_description))
    conn.commit()
    cur.close()
    conn.close()

def fetch_transactions(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT amount, category, description, timestamp
        FROM transactions
        WHERE user_id = %s
        ORDER BY timestamp DESC
    """, (user_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {
            "amount": row[0],
            "category": row[1],
            "description": decrypt_data(row[2]),
            "timestamp": row[3]
        }
        for row in rows
    ]

# 🔍 Diagnostic: test database connection
def test_db_connection():
    import streamlit as st

    db_user = os.getenv("DB_USER")
    db_name = os.getenv("DB_NAME")
    db_host = os.getenv("DB_HOST")

    if db_user and db_name and db_host:
        st.success("✅ Environment variables loaded.")
    else:
        st.error("❌ Environment variables not loaded.")

    try:
        conn = get_connection()
        st.success("✅ Successfully connected to the PostgreSQL database.")
        conn.close()
    except Exception as e:
        st.error(f"❌ Database connection failed: {e}")
