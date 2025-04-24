from flask import Flask, render_template, request, redirect, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages

DB_FILE = 'rvu_navigation.db'

# Ensure database and tables are created
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        email TEXT,
                        password TEXT)''')

    # Create faculty table
    cursor.execute('''CREATE TABLE IF NOT EXISTS faculty (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        email TEXT,
                        password TEXT,
                        department TEXT)''')

    # Create contact table
    cursor.execute('''CREATE TABLE IF NOT EXISTS contact (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        email TEXT,
                        message TEXT)''')

    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO contact (name, email, message) VALUES (?, ?, ?)", (name, email, message))
    conn.commit()
    conn.close()
    flash("Message submitted successfully!", "success")
    return redirect('/')

@app.route('/register_user', methods=['POST'])
def register_user():
    name = request.form['username']
    email = request.form['email']
    password = request.form['password']

    # Hash the password before storing
    hashed_password = generate_password_hash(password)

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, hashed_password))
    conn.commit()
    conn.close()
    flash("User registered successfully!", "success")
    return redirect('/')

@app.route('/register_faculty', methods=['POST'])
def register_faculty():
    name = request.form['faculty_name']
    email = request.form['faculty_email']
    password = request.form['faculty_password']
    department = request.form['department']

    # Hash the password before storing
    hashed_password = generate_password_hash(password)

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO faculty (name, email, password, department) VALUES (?, ?, ?, ?)", 
                   (name, email, hashed_password, department))
    conn.commit()
    conn.close()
    flash("Faculty registered successfully!", "success")
    return redirect('/')

@app.route('/update_password', methods=['POST'])
def update_password():
    email = request.form['email']
    new_password = request.form['new_password']

    # Hash the new password before storing
    hashed_password = generate_password_hash(new_password)

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password = ? WHERE email = ?", (hashed_password, email))
    cursor.execute("UPDATE faculty SET password = ? WHERE email = ?", (hashed_password, email))
    conn.commit()
    conn.close()
    flash("Password updated successfully!", "success")
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
