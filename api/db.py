import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    try:
        return psycopg2.connect(
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            host=os.getenv("HOST"),
            port=os.getenv("PORT"),
            dbname=os.getenv("DBNAME")
        )
    except Exception as e:
        raise RuntimeError(f"Database connection failed: {e}")

if __name__ == "__main__":
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT NOW();")
                print("Current Time:", cur.fetchone())
    except Exception as e:
        print(f"Error: {e}")
