from flask import (
   Flask, Blueprint, flash, g, redirect, render_template, request, url_for, session
)
import os 
print (os.getcwd())
import Life_Scorer.user as user
import Life_Scorer.interface as interface
from functools import wraps
import datetime
import Life_Scorer.tools as tools
import Life_Scorer.scoring as scoring

app = Flask(__name__)
app.secret_key =  'K%=y(Ta4'



def debug(func):
    print('wrapped')
    print(func.__name__,' in wrappe')
    func()

def get_user():
    return session['username']

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        #Changed below to use session instead of g.
        if 'username' not in session:
            print('no user in login required')
            return redirect(url_for('login'))

        return view(**kwargs)

    return wrapped_view


@app.route('/create_task', methods=('GET', 'POST'))
@login_required
def create_task():
    categories = interface.get_categories(get_user())
    if request.method == 'POST':
        print(request.form)
        taskname = request.form['taskname']
        points = request.form['points']
        #Need further testing or refactor of below (also error handling)
        r = {'recurring': 1 , 'non-recurring' : 0 }
        recur = r[request.form['recurring']]
        category = request.form['category']
        interface.add_task(taskname,points,category,recur,get_user())
        return redirect(url_for('show_log'))
    import sys #testing delate later
    return render_template('create_task.html',categories=categories, version =sys.version)
    

@app.route('/show_log')
@login_required
def show_log():
    log = interface.get_log(get_user())
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
        timestamp = int(request.form['timestamp']) #client local timestamp ms
        tzoffset = int(request.form['tzoffset'])   #for conversion from utc to client local
        dt = tools.convert_timestamp(timestamp, tzoffset)
        date = dt[0]
        time = dt[1]
        print('Date: ', date, 'Time: ', time)
        #TODO Maybe change the working so the taskid stay with it instead of having to reconvert as below
        task_id = interface.get_task_by_name(task_name, get_user())
        interface.log_task(task_id, qty, note,date, time, get_user())
        return redirect(url_for('show_month'))
        
    tasks = interface.read_tasks(get_user())
    return render_template('create_log.html', tasks=tasks)
    

@app.route('/')
def hello_world():
    return redirect(url_for('login'))


@app.route('/login', methods=('GET', 'POST'))
def login():
    if 'username' in session:
        return redirect(url_for('show_month'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user.validate_user (username,password):
            session['username'] = request.form['username']
            return redirect(url_for('show_month'))
    return render_template('auth/login.html')


@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        #Line below is to disable this function until
        #functionality supports multiple users (not allow to access others records)
        #return render_template('auth/register.html')
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        user.add_user(username,password,email)
        return redirect(url_for('show_log'))
    return render_template('auth/register.html')
    

@app.route('/logout', methods=('GET', 'POST'))
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for('login'))


@app.route('/edit_tasks')
@login_required
def edit_tasks():
    tasks = interface.read_tasks(get_user())
    return render_template('edit_tasks.html',tasks=tasks)

@app.route('/edit_task/<task_id>', methods=('GET', 'POST'))
@app.route('/edit_task')
@login_required
def edit_task(task_id=0):
    if request.method == 'POST':
        print(request.form)
        taskname = request.form['taskname']
        points = request.form['points']
        #Need further testing or refactor of below (also error handling)
        r = {'recurring': 1 , 'non-recurring' : 0 }
        recur = r[request.form['recurring']]
        category = request.form['category']
        interface.update_task(taskname,points,category,recur,task_id, get_user())
        return redirect(url_for('edit_tasks'))
    if task_id is not 0:
        task = interface.get_task(task_id, get_user())
    categories = interface.get_categories(get_user())
    return render_template('edit_task.html',task=task, categories=categories)

@app.route('/create_category', methods=('GET','POST'))
@login_required
def create_category():
    if request.method == 'POST':
        new_category = request.form['category']
        interface.add_category(new_category,get_user())
        return redirect(url_for('show_log'))
    return render_template('create_category.html')

@app.route('/show_month')
@login_required
def show_month():
    month = scoring.get_month_scores(get_user())
    scores = [x[1] for x in month]
    average = round(sum(scores)/len(scores))
    return render_template('show_month.html', month = month, average = average)
