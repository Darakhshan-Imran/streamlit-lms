import streamlit as st
import os
import base64
from dotenv import load_dotenv
import pandas as pd
import asyncpg

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
        connection = asyncpg.connect(conn_str)
        return connection
    except Exception as e:
        st.error(f"Error connecting to database: {e}")
        return None

def create_table():
    """Create the books table if it does not exist."""
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                author VARCHAR(255) NOT NULL,
                year INTEGER,
                available BOOLEAN DEFAULT TRUE
            );
        """)
        
        connection.commit()
        cursor.close()
        connection.close()

# Cache the background image to prevent reloading
@st.cache_resource
def get_cached_bg():
    background_image_path = "assets/library_bg.jpg"

    # Convert Image to Base64 for inline CSS
    with open(background_image_path, "rb") as img_file:
        encoded_bg = base64.b64encode(img_file.read()).decode()

    return f"""
    <style>
    /* Background Image */
    .stApp {{
        background: url("data:image/jpg;base64,{encoded_bg}") no-repeat center center fixed;
        background-size: cover;
        overflow: hidden; /* Hides overflow */
    }}
    </style>
    """

def home_page():
    # Apply cached background
    st.markdown(get_cached_bg(), unsafe_allow_html=True)

    st.markdown(
        """
        <h1 style="text-align: center; 
                   font-family: 'Georgia', serif; 
                   font-size: 3rem; 
                   font-weight: bold; 
                   color: white; 
                   margin-top: 8px;
                   margin-right: 30vh; /* Moves text to the left */
                   text-shadow: 4px 4px 2px rgba(0,0,0,0.6);"> 
            Welcome To The Library Management System
        </h1>

        <h2 style="text-align: center; 
                   font-family: 'Georgia', serif; 
                   font-size: 1.5rem; 
                   font-weight: semibold; 
                   color: white; 
                   margin-top: -10px;
                   margin-right: 30vh; /* Moves text to the left */
                   text-shadow: 2px 2px 4px #000000;"> 
           'An investment in knowledge pays the best interest.'
           <br> 
            <span style = "font-size: 1rem; font-style:italic; margin-top: 3px;">
            — Benjamin Franklin
            </span>
        </h2>
        """,
        unsafe_allow_html=True
    )

   
# Function for adding books in library db

def add_book(title, author, year, read_status, available, genre  ):
    """Insert a new book record."""
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO books (title, author, year, read_status, available, genre) VALUES (%s, %s, %s, %s, %s, %s)",
            (title, author, year, read_status, available, genre)
        )
        connection.commit()
        cursor.close()
        connection.close()

# Function to get books data by title or author

def get_books_by_query(search_value, search_by="title"):
    """Retrieve books from the database based on title or author."""
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        
        # Choose the query based on search type
        if search_by == "title":
            query = "SELECT * FROM books WHERE title ILIKE %s ORDER BY id"
        else:  # search_by == "author"
            query = "SELECT * FROM books WHERE author ILIKE %s ORDER BY id"
        
        cursor.execute(query, (f"%{search_value}%",))  # Case-insensitive search
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows
    return []

# Function to get all books data

def get_books():
    """Retrieve all book records."""
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM books")
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows
    return []

# Function to update books in library

def update_book(book_id, title, author, year, read_status, available, genre):
    """Update an existing book record."""
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE books SET title=%s, author=%s, year=%s, read_status=%s, available=%s, genre=%s WHERE id=%s",
            (title, author, year, read_status, available, genre, book_id)  # Corrected order
        )
        connection.commit()
        cursor.close()
        connection.close()


def remove_book(title, book_id=None):
    """Search for books by title and delete the selected book if book_id is provided."""
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        
        # If book_id is provided, delete the book
        if book_id:
            cursor.execute("DELETE FROM books WHERE id=%s", (book_id,))
            connection.commit()
            cursor.close()
            connection.close()
            return book_id  # Return deleted book ID

        # Otherwise, search for books matching the title
        cursor.execute("SELECT id, title FROM books WHERE title ILIKE %s", (f"%{title}%",))
        books = cursor.fetchall()
        cursor.close()
        connection.close()
        
        if not books:
            return None  # No matching books found
        return books  # Return list of books

# Function to show stats

def display_stats():
   """It shows stats of read books from the collection.""" 

   connection = get_connection()
   if connection:
        cursor = connection.cursor()

      #Get Total books count
        query_total = "SELECT COUNT(*) FROM Books"
        cursor.execute(query_total)
        total_books = cursor.fetchone()[0]

      #Get count of read books
        query_read = "SELECT COUNT(*) FROM Books WHERE read_status = 'read'"
        cursor.execute(query_read)
        read_books = cursor.fetchone()[0]
      
        cursor.close()
        connection.close()
        
        read_percentage = (read_books / total_books) * 100 if total_books > 0 else 0
        return total_books, read_books, read_percentage
      
    
# Create the table on startup
create_table()