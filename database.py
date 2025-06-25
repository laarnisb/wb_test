from sqlalchemy import create_engine, MetaData

DATABASE_URL = "sqlite:///wisebudget.db"
engine = create_engine(DATABASE_URL, echo=False)
metadata = MetaData()

def create_tables():
    with engine.connect() as connection:
        connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
        """)
        connection.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            amount TEXT NOT NULL,
            description TEXT
        );
        """)
