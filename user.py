import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash

#TODO need to rework how database is handled even if this works.

def get_db():
    conn = sqlite3.connect('user.db')
    #c = conn.cursor()
    return conn

def add_user(username,password,email):
    conn = get_db()
    c = conn.cursor()
    password = generate_password_hash(password)
    holder=(username,password,email)
    c.execute('INSERT INTO users (username,password,email) VALUES(?,?,?)',holder)
    conn.commit()

def validate_user(username, password):
    conn = get_db()
    c = conn.cursor()
    holder = (username,)
    user_pw = c.execute('SELECT password FROM users WHERE username=?',holder).fetchone()
    if user_pw:
        user_pw = user_pw[0]
    else:
        return False #Invalid usersame
    return check_password_hash(user_pw,password)
    
    