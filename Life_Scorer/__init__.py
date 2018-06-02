from flask import (
   Flask, Blueprint, flash, g, redirect, render_template, request, url_for, session
)
import os 
print (os.getcwd())
from Life_Scorer.user import add_user , validate_user 
from Life_Scorer.interface import get_log, read_tasks, log_task, get_task_by_name
from functools import wraps

app = Flask(__name__)
app.secret_key =  'K%=y(Ta4'
def debug(func):
    print('wrapped')
    print(func.__name__,' in wrappe')
    func()

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        #Changed below to use session instead of g. 
        if 'username' not in session:
            print('no user in login required')
            return redirect(url_for('login'))

        return view(**kwargs)

    return wrapped_view

@app.route('/show_log')
@login_required
def show_log():
    log = get_log()
    log.reverse() #So it shows latest record first
    return render_template('log.html', log=log)
    
@app.route('/index')
def index():
    return render_template('index')





@app.route('/create_log', methods=('GET', 'POST'))
@login_required
def create_log():
    if request.method == 'POST':
        note = request.form['notes']
        qty = request.form['quantity']
        task_name = request.form['selection']
        #TODO Maybe change the working so the taskid stay with it instead of having to reconvert as below
        task_id = get_task_by_name(task_name)
        log_task(task_id, qty, note)
        return redirect(url_for('show_log'))
        
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
