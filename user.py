import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash


db = None
conn = sqlite3.connect('user.db')
c = conn.cursor()

def add_user(username,password,email):
    password = generate_password_hash(password)
    holder=(username,password,email)
    c.execute('INSERT INTO users (username,password,email) VALUES(?,?,?)',holder)
    conn.commit()

def validate_user(username, password):
    holder = (username,)
    user_pw = c.execute('SELECT password FROM users WHERE username=?',holder).fetchone()
    if user_pw:
        user_pw = user_pw[0]
    else:
        return False #Invalid usersame
    return check_password_hash(user_pw,password)
    
    