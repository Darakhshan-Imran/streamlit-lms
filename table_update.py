import streamlit as st
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    """
    Connect to Neon using credentials from Streamlit secrets or .env.
    """
    if "neon" in st.secrets:
        conn_str = st.secrets["neon"]["url"]
    else:
        conn_str = os.getenv("NEON_DATABASE_URL")
    
    try:
        conn = psycopg2.connect(conn_str)
        return conn
    except Exception as e:
        st.error(f"Error connecting to database: {e}")
        return None

# def modify_books_table():
#     """Modify the books table by adding back 'available' and ensuring 'read_status' exists."""
#     conn = get_connection()
#     if conn:
#         cur = conn.cursor()

#         # Step 1: Add 'available' column if it does not exist
#         cur.execute("""
#             DO $$ 
#             BEGIN
#                 IF NOT EXISTS (
#                     SELECT 1 FROM information_schema.columns 
#                     WHERE table_name = 'books' AND column_name = 'available'
#                 ) THEN
#                     ALTER TABLE books ADD COLUMN available BOOLEAN DEFAULT TRUE;
#                 END IF;
#             END $$;
#         """)

#         # Step 2: Ensure 'read_status' column exists
#         cur.execute("""
#             DO $$ 
#             BEGIN
#                 IF NOT EXISTS (
#                     SELECT 1 FROM information_schema.columns 
#                     WHERE table_name = 'books' AND column_name = 'read_status'
#                 ) THEN
#                     ALTER TABLE books ADD COLUMN read_status VARCHAR(10) 
#                     CHECK (read_status IN ('read', 'unread')) DEFAULT 'unread';
#                 END IF;
#             END $$;
#         """)

#         conn.commit()
#         cur.close()
#         conn.close()
#         print("✅ Database modified: 'available' added back and 'read_status' ensured.")

# if __name__ == "__main__":
#     modify_books_table()
def modify_books_table():
    """Modify the books table by adding a 'genre' column if it does not exist."""
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        
        # Check if the 'genre' column already exists, then add it if not
        cursor.execute("""
            DO $$ 
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM information_schema.columns 
                    WHERE table_name = 'books' AND column_name = 'genre'
                ) THEN
                    ALTER TABLE books ADD COLUMN genre VARCHAR(100);
                END IF;
            END $$;
        """)

        connection.commit()
        cursor.close()
        connection.close()
        print("✅ 'genre' column added to books table.")

if __name__ == "__main__":
       # Ensure the table exists
    modify_books_table() # Modify the table by adding the 'genre' column