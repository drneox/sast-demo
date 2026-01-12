import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
# SECURITY WARNING: Use environment variable in production
# Example: app.secret_key = os.environ.get('SECRET_KEY')
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

DATABASE = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template('index.html', users=users)

@app.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        
        if not name or not email:
            flash('Name and email are required!')
            return redirect(url_for('add_user'))
        
        conn = get_db_connection()
        conn.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
        conn.commit()
        conn.close()
        
        flash('User added successfully!')
        return redirect(url_for('index'))
    
    return render_template('add_user.html')

@app.route('/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    flash('User deleted successfully!')
    return redirect(url_for('index'))

@app.route('/search')
def search_user():
    search_query = request.args.get('q', '')
    conn = get_db_connection()
    
    if search_query:
        # VULNERABILITY: SQL Injection - user input directly concatenated into SQL query
        # This is intentionally vulnerable for CodeQL testing purposes
        query = "SELECT * FROM users WHERE name LIKE '%" + search_query + "%' OR email LIKE '%" + search_query + "%'"
        users = conn.execute(query).fetchall()
    else:
        users = conn.execute('SELECT * FROM users').fetchall()
    
    conn.close()
    return render_template('index.html', users=users, search_query=search_query)

if __name__ == '__main__':
    init_db()
    # SECURITY WARNING: Debug mode should be disabled in production
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode)
