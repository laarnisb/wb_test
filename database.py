import os
import psycopg2

def insert_transaction(user_id, amount, category, description):
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO transactions (user_id, amount, category, description) VALUES (%s, %s, %s, %s)",
        (user_id, amount, category, description)
    )
    conn.commit()
    cur.close()
    conn.close()
