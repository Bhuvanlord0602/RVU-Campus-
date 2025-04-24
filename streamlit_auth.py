# streamlit_auth.py
import streamlit as st
import subprocess
import time
import sqlite3

DB_FILE = 'rvu_navigation.db'

# Initialize DB
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Create user login function
def authenticate(username, password):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE name=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

# Create user registration function
def register_user(username, password):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

# UI setup
st.set_page_config(page_title="RVU Login", page_icon="🔐", layout="centered")
st.title("🔐 RVU Campus Portal")

menu = st.sidebar.radio("Navigation", ["Login", "Register"])

init_db()  # Ensure DB exists

if menu == "Login":
    st.subheader("🔑 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = authenticate(username, password)
        if user:
            st.success("Login successful!")
            st.balloons()
            st.write("Launching Flask application...")

            subprocess.Popen(["python", "app.py"])
            time.sleep(2)

            st.markdown("---")
            st.markdown("### Flask App:")
            st.markdown("[Open Flask App](http://localhost:5000)", unsafe_allow_html=True)
            st.components.v1.iframe("http://localhost:5000", height=600)
        else:
            st.error("Invalid credentials. Try again.")

elif menu == "Register":
    st.subheader("📝 Register")
    new_user = st.text_input("Choose a username")
    new_password = st.text_input("Choose a password", type="password")

    if st.button("Register"):
        if register_user(new_user, new_password):
            st.success("Account created! Please log in.")
            st.info("Go to the Login tab.")
        else:
            st.warning("Username already exists. Please try another.")
