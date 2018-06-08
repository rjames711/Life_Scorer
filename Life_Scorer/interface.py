#!/usr/bin/env python3
#TODO Think of new name for tasks and refactor
#TODO Implement menu by category
#TODO Add some functionality for plain notes
#TODO Add functionality to view days score 
#Maybe rename file

import sqlite3, os

class Task:
    def __init__(self, task_id, name, points, category, recurring, display):
        self.task_id = task_id
        self.name = name
        self.points = points
        self.category = category
        self.recurring = recurring
        self.display = display
    
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

def get_task_db():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'test.db')
    if os.path.exists(filename):
        return sqlite3.connect(filename)
    else:
        conn = sqlite3.connect(filename)
        c = conn.cursor()
        exec_sql(c,'schema.sql')
        return conn


def read_tasks():
    conn = get_task_db()
    c = conn.cursor()
    c.execute('select id,name,points,categories_id,recurring,display from tasks')
    tasks = c.fetchall()
    task_list = [ Task(*x) for x in tasks ] 
    return task_list

#TODO this returns task id. Should return a task need to refactor
#Returns task id from task name
def get_task_by_name(task_name):
    conn = get_task_db()
    c = conn.cursor()
    c.execute('SELECT id FROM tasks WHERE name=?',(task_name,))
    task_id = c.fetchone()
    return task_id[0]

#Return task object from task id 
def get_task(task_id):
    conn = get_task_db()
    c = conn.cursor()
    c.execute( 'SELECT * FROM tasks WHERE id = ?', (task_id,))
    task = c.fetchone()
    return Task(*task)


def log_task(task_id, qty, note, date, time):
    print('entering log', task_id,qty, note)
    holder = ( task_id, qty, note, date, time)
    conn = get_task_db()
    c = conn.cursor()
    c.execute('insert into log (task_id, qty, note, date, time) values(?,?,?,?,?)',holder)
    task = get_task(task_id)    
    if not task.recurring:
            task.display = 0
            c.execute('update tasks set display = 0 where id = ?',(str(task.task_id),))
            conn.commit()
    conn.commit()


def get_log():
    conn = get_task_db()
    c = conn.cursor()
    c.execute("select tasks.name, log.qty, log.date, log.time, log.note from tasks inner join log on log.task_id=tasks.id")
    return c.fetchall()

def show_log():
    log = get_log()
    print('Qty\tTask')
    print(5*'-'+'\t'+5*'-')
    for i in log: print(i[1],'\t', i[0],'\t',i[2])
    print()


def add_category(name):
    holder =(name,)
    conn = get_task_db()
    c = conn.cursor()
    c.execute('insert into categories (name) values(?)',holder)
    conn.commit()


def get_categories():
    conn = get_task_db()
    c = conn.cursor()
    c.execute('select * from categories')
    return c.fetchall()


#Update task attributes based on id
def update_task(name,points, category, recurring, id):
    holder =(name,points,category,recurring,id)
    conn = get_task_db()
    c = conn.cursor()
    c.execute('update tasks set name = ?, points = ?, categories_id = ?, recurring = ? where id = ?' ,holder)
    conn.commit()

def add_task(name,points, category, recurring):
    holder =(name,points,category,recurring)
    conn = get_task_db()
    c = conn.cursor()
    c.execute('insert into tasks (name,points,categories_id, recurring) values(?,?,?,?)',holder)
    conn.commit()

