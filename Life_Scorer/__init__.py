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
import Life_Scorer.sum_by_day as sum_by_day
import Life_Scorer.custom_stats as cus_stats_module
import json

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
        attributes = {}
        i=1
        while 'attribute_name-'+str(i) in request.form:
            name = request.form['attribute_name-'+str(i)]
            attributes[name] ={}
            attributes[name]['min'] = request.form['min-'+str(i)]
            attributes[name]['max'] = request.form['max-'+str(i)]
            attributes[name]['default'] = request.form['default-'+str(i)]
            attributes[name]['scored'] = request.form['scored-'+str(i)]
            #print(json.dumps(attributes))
            i+=1
        taskname = request.form['taskname']
        description = request.form['description']
        points = request.form['points']
        #Need further testing or refactor of below (also error handling)
        r = {'recurring': 1 , 'non-recurring' : 0 }
        recur = r[request.form['recurring']]
        category = request.form['category']
        interface.add_task(taskname, points, category, recur, 
        json.dumps(attributes),description, get_user())
        return redirect(url_for('create_log'))

    import sys #testing delate later
    return render_template('create_task.html',categories=categories, version =sys.version)
    

@app.route('/show_log')
@login_required
def show_log():
    log = interface.get_log(get_user())
    log.reverse() #So it shows latest record first
    return render_template('log.html', log=log)

@app.route('/show_task/<tasks>')
@app.route('/show_task')
@login_required
def show_task(tasks):
    tasks = tasks.split('&')
    for i in range(len(tasks)):
        name=tasks[i]
        tid = interface.get_task_by_name(name,get_user())
        #really confusing, basicaly getting task_id if task_name is passed in instead
        if tid:
            tasks[i] = tid
    print(tasks) 
    log=[]
    for t in tasks:
        log += interface.get_log_history(t, get_user())
    print(log)
    log.sort(key=lambda x: x[0]) #Sorting by id
    log.reverse() #So it shows latest record first
    return render_template('task_history.html', log=log)
 
@app.route('/show_log/<int:num_logs>')
@login_required
def show_log_part(num_logs):
    log = interface.get_log(get_user())
    log.reverse() #So it shows latest record first
    log = log[0:num_logs]  
    return render_template('log.html', log=log)
    
@app.route('/index')
def index():
    return render_template('index')


@app.route('/create_log', methods=('GET', 'POST'))
@login_required
def create_log():
    if request.method == 'POST':
        form = dict(request.form)
        #print(form)
        #debug(anerror) #error for sake of error to trigger debugger.
        note = form.pop('notes')
        task_name = form.pop('selection')
        timestamp = int(form.pop('timestamp')) #client local timestamp ms
        tzoffset = int(form.pop('tzoffset'))   #for conversion from utc to client local
        dt = tools.convert_timestamp(timestamp, tzoffset)
        date = dt[0]
        time = dt[1]
        #dont judge. This is so they still show up as ints when pulled directly from db 
        def get_number(s):
            n=float(s)
            return int(n) if n.is_integer() else n
        form = { key:get_number(val) for key, val in form.items() }
        attributes = json.dumps(form)
        #print(attributes)
        #TODO Maybe change the working so the taskid stay with it instead of having to reconvert as below
        task_id = interface.get_task_by_name(task_name, get_user())
        interface.log_task(task_id, attributes, note, date, time, get_user())
        return redirect(url_for('create_log'))
        
    #tasks = interface.read_tasks(get_user())
    import Life_Scorer.rate_tasks as rate_tasks
    tasks = rate_tasks.sort_tasks(250,get_user())
    attr = {task.name:task.attributes for task in tasks}
    attr = json.dumps(attr)
    dt = datetime.datetime.utcnow() -datetime.timedelta(hours=5)
    score = scoring.get_day_score(dt.date(),get_user())
    return render_template('create_log.html', tasks=tasks, attr=attr, score=score)
    

@app.route('/')
def hello_world():
    return redirect(url_for('login'))


@app.route('/login', methods=('GET', 'POST'))
def login():
    if 'username' in session:
        return redirect(url_for('create_log'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user.validate_user (username,password):
            session['username'] = request.form['username']
            return redirect(url_for('create_log'))
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
    is_id = interface.get_task_by_name(task_id, get_user()) 
    #Basically sloppy way to get request to work with either id or name
    if is_id:
        task_id = is_id
    if request.method == 'POST':
        attributes = {}
        i=1
        while 'attribute_name-'+str(i) in request.form:
            name = request.form['attribute_name-'+str(i)]
            attributes[name] ={}
            attributes[name]['min'] = request.form['min-'+str(i)]
            attributes[name]['max'] = request.form['max-'+str(i)]
            attributes[name]['default'] = request.form['default-'+str(i)]
            attributes[name]['scored'] = request.form['scored-'+str(i)]
            #print(json.dumps(attributes))
            i+=1
        taskname = request.form['taskname']
        description = request.form['description']
        points = request.form['points']
        #Need further testing or refactor of below (also error handling)
        r = {'recurring': 1 , 'non-recurring' : 0 }
        recur = r[request.form['recurring']]
        category = request.form['category']
        d = {'display': 1 , 'hide' : 0 }
        display = d[request.form['display']]
        
        interface.update_task(taskname, points, category, recur, 
        json.dumps(attributes),task_id,display,description, get_user())
        return redirect(url_for('create_log'))
    if task_id is not 0:
        task = interface.get_task(task_id, get_user())
    categories = interface.get_categories(get_user())
    attr = task.attributes
    attr = json.dumps(attr)
    return render_template('edit_task.html',task=task, categories=categories,attr=attr)

@app.route('/create_category', methods=('GET','POST'))
@login_required
def create_category():
    if request.method == 'POST':
        new_category = request.form['category']
        interface.add_category(new_category,get_user())
        return redirect(url_for('create_log'))
    return render_template('create_category.html')

@app.route('/show_month')
@login_required
def show_month():
    month = scoring.get_month_scores(get_user())
    scores = [x[1] for x in month]
    average = round(sum(scores)/len(scores))
    #Below method of get todays score could break if out of order
    #TODO get todays score by dictionary method instead of just last score in list
    todays_score = scores[0]
    return render_template('show_month.html', 
    month = month, average = average, todays_score = todays_score)

@app.route('/edit_log/<int:log_id>', methods=('GET','POST'))
@login_required
def edit_log(log_id):
    if request.method == 'POST':
        form = dict(request.form)
        #print(form)
        #debug(anerror) #error for sake of error to trigger debugger.
        note = form.pop('note')
        task_id = form.pop('task_id')
        date = form.pop('date')
        time = form.pop('time')
        attributes=form.pop('attributes')
        interface.update_log(log_id,task_id,note,date,time,attributes,get_user())
        return redirect(url_for('show_log_part',num_logs =50))
    a_log = interface.get_log_by_id(log_id, get_user())[0]
    return render_template('edit_log.html', a_log =a_log)

@app.route('/graph/<task_id>')
@app.route('/graph')
@login_required
def graph(task_id):
    name=task_id
    name = interface.get_task_by_name(name,get_user())
    #really confusing, basicaly getting task_id if task_name is passed in instead
    if name:
        task_id = name 
    task_id=int(task_id)
    conn = interface.get_task_db(get_user())
    c = conn.cursor()
    if task_id ==-1:
        data={}
        data['points']=cus_stats_module.get_monthly_scores(get_user())
        dates = [ d[1] for d in data['points']]
        data['points'] = [x[0] for x in data['points']]
        data['average'] = [ x/30 for x in data['points']]
        return render_template('graph.html',data=data, dates=dates)

    if task_id == 0:
        data={}
        data['points']=cus_stats_module.get_weekly_scores(get_user())
        dates = [ d[1] for d in data['points']]
        data['points'] = [x[0] for x in data['points']]
        return render_template('graph.html',data=data, dates=dates)

    c.execute('select attributes, date from log where task_id =?',(task_id,))
    r = c.fetchall()
    attrs = [json.loads(x[0]) for x in r]
    data = {}
    for dp in attrs:
        for attr in dp:
            if attr in data:
                data[attr].append(dp[attr])
            else:
                data[attr] = [dp[attr]]
    
    dates = [y[1] for y in r]
    data['points']=[]
    for day in dates:
        data['points'].append(scoring.get_day_score_by_task(day,get_user(),task_id))
    #d = [datetime.datetime.strptime(x,'%Y-%m-%d') for x in d]
    #start=d[1]
    #d = [(x-start).days for x in d]
    #d=json.dumps(d)
    return render_template('graph.html',data=data, dates=dates)


@app.route('/choose_graph')
@login_required
def choose_graph():
    tasks = interface.read_tasks(get_user())
    return render_template('choose_graph.html',tasks=tasks)

@app.route('/choose_task')
@login_required
def choose_task():
    tasks = interface.read_tasks(get_user())
    return render_template('choose_task.html',tasks=tasks)

@app.route('/day_sums/<int:num_days>')
@login_required
def day_sums(num_days):
    days = tools.get_days(num_days,0)
    days_sums={}
    for day in days:
        days_sums[day] = sum_by_day.get_sums_by_day(day, get_user())
    return render_template('day_sums.html', days_sums=days_sums)

@app.route('/week_sums/<int:num_weeks>')
@login_required
def week_sums(num_weeks):
    week_sums={}
    for week in range(num_weeks):
        days = tools.get_days(7,7*week)
        week_range = days[0] + ' - ' + days[len(days)-1]
        week_sums[week_range] = sum_by_day.get_days_sums(days, get_user())
    #TODO below is kinda weird just using day sums template and variable
    return render_template('day_sums.html', days_sums=week_sums)



@app.route('/month_sums/<int:num_months>')
@login_required
def month_sums(num_months):
    month_sums={}
    for month in range(num_months):
        days = tools.get_days(30,30*month)
        month_range = days[0] + ' - ' + days[len(days)-1]
        month_sums[month_range] = sum_by_day.get_days_sums(days, get_user())
    #TODO below is kinda weird just using day sums template and variable
    return render_template('day_sums.html', days_sums=month_sums)


@app.route('/create_log2')
def create_log2():
    tasks = interface.read_tasks(get_user())
    tasks = [task.__dict__ for task in tasks]
    return render_template('create_log2.html', tasks = tasks)


@app.route('/api')
def api():
    #tasks = interface.read_tasks(get_user())
    tasks = interface.read_tasks('Rob')
    tasks = [task.__dict__ for task in tasks]
    return json.dumps(tasks)

#Custom statistic page with potentially hardcoded values for personal use
@app.route('/custom_stats')
def custom_stats():
    def ave_weight(sums):
        k = ('weight','qty') #key
        return sums[0][k]/sums[1][k]
    ave_weight_week1 = ave_weight(sum_by_day.get_days_sums_by_task(tools.get_days(7,0),get_user(),14))
    ave_weight_week2 = ave_weight(sum_by_day.get_days_sums_by_task(tools.get_days(7,7),get_user(),14))
    exercise_points_week = sum([scoring.get_day_score_by_category(x,get_user(),1) 
        for x in tools.get_days(7,0)])
    points_week_total = sum([scoring.get_day_score(x,get_user()) for x in tools.get_days(7,0)])
    return render_template('custom_stats.html', w1=ave_weight_week1,
    w2=ave_weight_week2,exp=exercise_points_week,tp=points_week_total)
    
#For even more ephemeral purposes than custom stats.
@app.route('/temp')
def temp():
    conn = interface.get_task_db(get_user())
    c = conn.cursor()
    c.execute("select log.id, tasks.name, log.attributes, log.date, log.time, log.note from tasks inner join log on log.task_id=tasks.id where date='2019-01-01'")
    log = c.fetchall()
    log.reverse() #So it shows latest record first
    return render_template('log.html', log=log)

@app.route('/choose_script')
def choose_script():
    scripts = interface.get_scripts(get_user())
    scripts = [x[0] for x in scripts] # just need names
    if len(scripts)==0:
        scripts.append('first_script')
        interface.add_edit_script(get_user(),scripts[0],'console.log("edit me")')
    print(scripts)
    return render_template('choose_script.html',scripts=scripts)

@app.route('/custom/<script_name>')
def custom(script_name):
    print(script_name)
    script = interface.get_script(get_user(), script_name)
    return render_template('custom.html', script_name=script_name, script=script)

@app.route('/save_script',methods=('POST',))
def save_script():
    name = request.form['script_name']
    script = request.form['script']
    interface.add_edit_script(get_user(),name,script)
    print(name)
    #return redirect(url_for('custom',script_name=name))
    return redirect(url_for('misc'))


@app.route('/misc')
def misc():
    return render_template('misc.html')
