import streamlit as st
import json
import os

# Set page config
st.set_page_config(page_title="📚 Personal Library Manager", layout="centered")

# ---------- Utilities ----------
LIBRARY_FILE = "library.json"

def load_library():
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, "r") as f:
            return json.load(f)
    return []

def save_library(library):
    with open(LIBRARY_FILE, "w") as f:
        json.dump(library, f, indent=4)

def book_format(book, idx):
    return f"**{idx+1}. {book['title']}** by *{book['author']}* ({book['year']}) - {book['genre']} - {'✅ Read' if book['read'] else '📖 Unread'}"

# Load data
if 'library' not in st.session_state:
    st.session_state.library = load_library()

# ---------- App UI ----------
st.title("📚 Personal Library Manager")
menu = st.sidebar.radio("Choose an option", [
    "Add a Book", "Remove a Book", "Search", "Display All Books", "Statistics", "Exit"
])

library = st.session_state.library

# ---------- Add Book ----------
if menu == "Add a Book":
    st.subheader("➕ Add a New Book")
    with st.form("add_book"):
        title = st.text_input("Title")
        author = st.text_input("Author")
        year = st.number_input("Publication Year", min_value=0, step=1)
        genre = st.text_input("Genre")
        read = st.radio("Have you read this book?", ["Yes", "No"]) == "Yes"
        submitted = st.form_submit_button("Add Book")

        if submitted:
            new_book = {
                "title": title.strip(),
                "author": author.strip(),
                "year": int(year),
                "genre": genre.strip(),
                "read": read
            }
            library.append(new_book)
            save_library(library)
            st.success("✅ Book added successfully!")

# ---------- Remove Book ----------
elif menu == "Remove a Book":
    st.subheader("🗑️ Remove a Book")
    titles = [book["title"] for book in library]
    if titles:
        selected = st.selectbox("Select a book to remove", titles)
        if st.button("Remove"):
            library[:] = [book for book in library if book["title"] != selected]
            save_library(library)
            st.success("❌ Book removed successfully!")
    else:
        st.info("Your library is empty.")

# ---------- Search ----------
elif menu == "Search":
    st.subheader("🔍 Search for a Book")
    method = st.radio("Search by", ["Title", "Author"])
    query = st.text_input("Enter search term")
    if query:
        results = [
            book for book in library
            if query.lower() in book[method.lower()].lower()
        ]
        if results:
            for idx, book in enumerate(results):
                st.markdown(book_format(book, idx))
        else:
            st.warning("No matching books found.")

# ---------- Display All ----------
elif menu == "Display All Books":
    st.subheader("📖 Your Library")
    if library:
        for idx, book in enumerate(library):
            st.markdown(book_format(book, idx))
    else:
        st.info("No books in your library yet.")

# ---------- Stats ----------
elif menu == "Statistics":
    st.subheader("📊 Library Statistics")
    total = len(library)
    read_count = sum(1 for book in library if book["read"])
    percent = (read_count / total * 100) if total > 0 else 0
    st.write(f"**Total Books:** {total}")
    st.write(f"**Read:** {read_count} ({percent:.1f}%)")

# ---------- Exit ----------
elif menu == "Exit":
    save_library(library)
    st.success("✅ Library saved to file. Goodbye!")
