import streamlit as st
import psycopg2
import os
from dotenv import load_dotenv
import pandas as pd

# Load environment variables (for local development)
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

def create_table():
    """Create the books table if it does not exist."""
    conn = get_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                author VARCHAR(255) NOT NULL,
                year INTEGER,
                available BOOLEAN DEFAULT TRUE
            );
        """)
        conn.commit()
        cur.close()
        conn.close()

def add_book(title, author, year, available):
    """Insert a new book record."""
    conn = get_connection()
    if conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO books (title, author, year, available) VALUES (%s, %s, %s, %s)",
            (title, author, year, available)
        )
        conn.commit()
        cur.close()
        conn.close()

def get_books():
    """Retrieve all book records."""
    conn = get_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM books ORDER BY id")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    return []

def update_book(book_id, title, author, year, available):
    """Update an existing book record."""
    conn = get_connection()
    if conn:
        cur = conn.cursor()
        cur.execute(
            "UPDATE books SET title=%s, author=%s, year=%s, available=%s WHERE id=%s",
            (title, author, year, available, book_id)
        )
        conn.commit()
        cur.close()
        conn.close()

def delete_book(book_id):
    """Delete a book record."""
    conn = get_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM books WHERE id=%s", (book_id,))
        conn.commit()
        cur.close()
        conn.close()

# Create the table on startup
create_table()

st.title("Library Management System")

# Sidebar menu for navigation
menu = ["Add Book", "View Books", "Update Book", "Delete Book"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add Book":
    st.header("Add a New Book")
    with st.form("add_book_form"):
        title = st.text_input("Title")
        author = st.text_input("Author")
        year = st.number_input("Year", min_value=1000, max_value=2100, step=1)
        available = st.checkbox("Available", value=True)
        submitted = st.form_submit_button("Add Book")
        if submitted:
            if title and author:
                add_book(title, author, year, available)
                st.success(f"Book '{title}' added successfully!")
            else:
                st.error("Title and Author are required.")

elif choice == "View Books":
    st.header("View Books")
    books = get_books()
    if books:
        df = pd.DataFrame(books, columns=["ID", "Title", "Author", "Year", "Available"])
        st.dataframe(df)
    else:
        st.info("No books found in the database.")

elif choice == "Update Book":
    st.header("Update Book")
    book_id = st.number_input("Enter Book ID to update", min_value=1, step=1)
    if st.button("Fetch Book"):
        books = get_books()
        book = next((b for b in books if b[0] == book_id), None)
        if book:
            with st.form("update_book_form"):
                title = st.text_input("Title", value=book[1])
                author = st.text_input("Author", value=book[2])
                year = st.number_input("Year", min_value=1000, max_value=2100, step=1, value=book[3] if book[3] else 2000)
                available = st.checkbox("Available", value=book[4])
                submitted = st.form_submit_button("Update Book")
                if submitted:
                    update_book(book_id, title, author, year, available)
                    st.success(f"Book ID {book_id} updated successfully!")
        else:
            st.error("Book not found.")

elif choice == "Delete Book":
    st.header("Delete Book")
    book_id = st.number_input("Enter Book ID to delete", min_value=1, step=1)
    if st.button("Delete Book"):
        delete_book(book_id)
        st.success(f"Book ID {book_id} deleted successfully!")
