import sqlite3, os
from werkzeug.security import check_password_hash, generate_password_hash

#TODO need to rework how database is handled even if this works.

def exec_sql(c, sql_file):
    dirname = os.path.dirname(__file__)
    sql_file = os.path.join(dirname, sql_file)
    sql = open(sql_file)
    sql = sql.read()
    sql = sql.split(';')
    for statement in sql:
        c.execute(statement)

def get_db():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'user.db')
    if os.path.exists(filename):
        return sqlite3.connect(filename)
    else:
        conn = sqlite3.connect(filename)
        c = conn.cursor()
        exec_sql(c,'user.sql')
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
    
def change_password(username, password):
    conn = get_db()
    c = conn.cursor()
    password = generate_password_hash(password)
    holder=(password, username)
    c.execute("UPDATE users SET password = ? WHERE username = ?", holder)
    conn.commit()

