#!/usr/bin/env python3
#TODO Think of new name for tasks and refactor
#TODO Implement menu by category
#TODO Add some functionality for plain notes
#TODO Add functionality to view days score 
#Maybe rename file

import sqlite3, os, json

class Task:
    def __init__(self, task_id, name, points, category, recurring, display, attributes, description):
        self.task_id = task_id
        self.name = name
        self.points = points
        self.category = category
        self.recurring = recurring
        self.display = display
        self.attributes = json.loads(attributes)
        self.description = description
    
    def __repr__(self):
        return str(self.task_id) + ': ' + self.name



#TODO DRY move this and the one in user.py to its own file or something
def exec_sql(c, sql_file):
    dirname = os.path.dirname(__file__)
    sql_file = os.path.join(dirname, sql_file)
    sql = open(sql_file)
    sql = sql.read()
    sql = sql.split(';')
    for statement in sql:
        c.execute(statement)

def get_task_db(user):
    db_file = 'db_files/'+user+'.db'
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, db_file)
    if os.path.exists(filename):
        return sqlite3.connect(filename)
    else:
        conn = sqlite3.connect(filename)
        c = conn.cursor()
        exec_sql(c,'schema.sql')
        return conn


def read_tasks(user):
    conn = get_task_db(user)
    c = conn.cursor()
    c.execute('''select id,name,points,categories_id
    ,recurring,display, attributes,description from tasks''')
    tasks = c.fetchall()
    task_list = [ Task(*x) for x in tasks ] 
    return task_list

#TODO this returns task id. Should return a task need to refactor
#Returns task id from task name, false if not in db
def get_task_by_name(task_name, user):
    conn = get_task_db(user)
    c = conn.cursor()
    c.execute('SELECT id FROM tasks WHERE name=?',(task_name,))
    task_id = c.fetchone()
    if task_id:
        return task_id[0]
    else:
        return False

#Return task object from task id 
def get_task(task_id, user):
    conn = get_task_db(user)
    c = conn.cursor()
    c.execute( 'SELECT * FROM tasks WHERE id = ?', (task_id,))
    task = c.fetchone()
    return Task(*task)


def log_task(task_id, attributes, note, date, time,user):
    print('entering log', task_id,attributes, note)
    holder = ( task_id, attributes, note, date, time)
    conn = get_task_db(user)
    c = conn.cursor()
    c.execute('insert into log (task_id, attributes, note, date, time) values(?,?,?,?,?)',holder)
    task = get_task(task_id, user)    
    if not task.recurring:
            task.display = 0
            c.execute('update tasks set display = 0 where id = ?',(str(task.task_id),))
            conn.commit()
    conn.commit()


def get_log(user):
    conn = get_task_db(user)
    c = conn.cursor()
    c.execute("select log.id, tasks.name, log.attributes, log.date, log.time, log.note from tasks inner join log on log.task_id=tasks.id")
    return c.fetchall()

def get_log_history(task_id, user):
    conn = get_task_db(user)
    c = conn.cursor()
    c.execute("select log.id, tasks.name, log.attributes, log.date, log.time, log.note from tasks inner join log on log.task_id=tasks.id where task_id=?",(task_id,))
    return c.fetchall()


def show_log(user):
    log = get_log(user)
    print('Qty\tTask')
    print(5*'-'+'\t'+5*'-')
    for i in log: print(i[1],'\t', i[0],'\t',i[2])
    print()

def get_log_by_id(id,user):
    conn = get_task_db(user)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM log where id=?",(id,))
    return c.fetchall()

def add_category(name,user):
    holder =(name,)
    conn = get_task_db(user)
    c = conn.cursor()
    c.execute('insert into categories (name) values(?)',holder)
    conn.commit()


def get_categories(user):
    conn = get_task_db(user)
    c = conn.cursor()
    c.execute('select * from categories')
    return c.fetchall()


#Update task attributes based on id
def update_task(name,points, category, recurring, attributes, id, display, description ,user):
    holder =(name,points,category,recurring, attributes, display, description, id)
    conn = get_task_db(user)
    c = conn.cursor()
    c.execute('update tasks set name = ?, points = ?, categories_id = ?, recurring = ?, attributes = ?,display = ?,description=? where id = ?' ,holder)
    conn.commit()

def update_log(log_id, task_id, note,date,time,attributes,user):
    holder = (task_id, note,date,time,attributes,log_id)
    conn = get_task_db(user)
    c = conn.cursor()
    c.execute('UPDATE log SET task_id=?,note=?,date=?,time=?,attributes=? WHERE id=?',holder)
    conn.commit()

def add_task(name,points, category, recurring, attributes,description, user):
    holder =(name,points,category,recurring, attributes,description)
    conn = get_task_db(user)
    c = conn.cursor()
    c.execute('insert into tasks (name,points,categories_id, recurring, attributes,description) values(?,?,?,?,?,?)',holder)
    conn.commit()

#Renames all the necessary log records when a rename is done on attribute
#A questionable strategy to be sure but here we are.
def rename_attribute(task_name, old_name,new_name, user):
    conn = get_task_db(user)
    c = conn.cursor()
    task = get_task_by_name(task_name, user)
    c.execute('select attributes, id from log where task_id=?',(task,))
    results = c.fetchall()
    for item in results:
        item = list(item)
        attr=json.loads(item[0])
        if old_name in attr:
            attr[new_name] = attr.pop(old_name)
            item[0] = json.dumps(attr)
        item = tuple(item)
        c.execute('update log set attributes=? where id =?', item)
        print(item)
    conn.commit()
    return results

def get_scripts(user):
    conn = get_task_db(user)
    c = conn.cursor()
    c.execute("SELECT script_name, script from scripts")
    log = c.fetchall()
    return log

def add_edit_script(user,script_name, script):
    conn = get_task_db(user)
    c = conn.cursor()
    try:#script exists: edit 
        get_script(user, script_name)
        c.execute("UPDATE scripts SET script=? where script_name=?",(script,script_name))
    except: #script doesn't exist: add    
        c.execute("INSERT INTO scripts (script_name, script ) VALUES (?,?)",(script_name,script))
    conn.commit()

def get_script(user, script_name):
    conn = get_task_db(user)
    c = conn.cursor()
    c.execute("SELECT script from scripts where script_name=?",(script_name,))
    return c.fetchall()[0][0]


    
