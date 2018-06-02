from flask import (
   Flask, Blueprint, flash, g, redirect, render_template, request, url_for, session
)

from user import add_user , validate_user 
from interface import get_log, read_tasks

app = Flask(__name__)
app.secret_key =  'K%=y(Ta4'
def debug(func):
    print('wrapped')
    print(func.__name__,' in wrappe')
    func()

@app.route('/show_log')
def show_log():
    log = get_log()
    return render_template('log.html', log=log)
    
@app.route('/index')
def index():
    return render_template('index')

@app.route('/create_log', methods=('GET', 'POST'))
def create_log():
    if request.method == 'POST':
        print (request)
        print(request.form['submit'])
    tasks = read_tasks()
    return render_template('create_log.html', tasks=tasks)
    

@app.route('/')
def hello_world():
    return redirect(url_for('login'))

@app.route('/hello')
def hello_world2():
    return 'Hello, World!2222222'

@app.route('/login', methods=('GET', 'POST'))
def login():
    if 'username' in session:
        return render_template('base.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if validate_user(username,password):
            session['username'] = request.form['username']
            return redirect(url_for('show_log'))
    return render_template('auth/login.html')

@app.route('/register')
def register():
    return render_template('auth/register.html')
    
@app.route('/logout')
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for('login'))

app.route('')