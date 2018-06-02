#!/usr/bin/env python3
#TODO Think of new name for tasks and refactor
#TODO Implement menu by category
#TODO Add some functionality for plain notes
#TODO Add functionality to view days score 
#Maybe rename file

import sqlite3

class Task:
    def __init__(self, task_id, name, points, category, recurring, display):
        self.task_id = task_id
        self.name = name
        self.points = points
        self.category = category
        self.recurring = recurring
        self.display = display


def get_task_db():
    return sqlite3.connect('test.db')
    

def read_tasks():
    conn = get_task_db()
    c = conn.cursor()
    c.execute('select id,name,points,categories_id,recurring,display from tasks')
    tasks = c.fetchall()
    task_list = [ Task(*x) for x in tasks ] 
    return task_list

def get_task_by_name(task_name):
    conn = get_task_db()
    c = conn.cursor()
    c.execute('SELECT id FROM tasks WHERE name=?',(task_name,))
    task_id = c.fetchone()
    return task_id[0]

def log_task(task_id, qty, note):
    print('entering log', task_id,qty, note)
    holder = (task_id,qty,note)
    conn = get_task_db()
    c = conn.cursor()
    c.execute('insert into log (task_id, qty, note) values(?,?,?)',holder)
    conn.commit()


def log_tasks_tui():
    conn = get_task_db()
    c = conn.cursor()
    print()
    tasks  = read_tasks()
    for t in tasks: 
        if t.display: 
            print(t.task_id,': ',t.name,t.recurring)
    task = input('Select a task: ')
    qty = input('Enter a quantity: ')
    note = input('Enter a note: ')
    task = tasks[int(task)-1]
    #TODO will need to update here if task list changed to dict (indexing could conflict)
    #Otherwise if list style is kept could keep this implentation but change what is
    # passed back to db to task.id instead of the raw user input (this may be better)
    confirm = input('Confirm submit task "' + task.name + 
            '" with qty '+qty+ ' (y/n): ' )
    if confirm == 'y':
        log_task(task.task_id, qty, note)
        conn.commit()
        #TODO This should be be happnening in log task since this will only happne in tui
        if not task.recurring:
            task.display = 0
            c.execute('update tasks set display = 0 where id = ?',(str(task.task_id),))
            conn.commit()
    else:
        print('canceled')

def get_log():
    conn = get_task_db()
    c = conn.cursor()
    c.execute("select tasks.name, log.qty, log.timestamp, log.note from tasks inner join log on log.task_id=tasks.id")
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


def add_category_tui():
    name = input('Enter new category name: ')
    add_category(name)


#TODO finish implementing one time task functionality
def add_task_tui():
    conn = get_task_db()
    c = conn.cursor()
    c.execute('select * from categories')
    categories = c.fetchall()
    name = input('Enter new task name: ')
    points = input('Enter point value: ')
    print (categories)
    category = input('Select a category: ') 
    print('1: One Time Task 2: Recurring task')
    recurring = input('Select task type: ')
    recurring = int(recurring) - 1  
    add_task(name,points,category, recurring)


def add_task(name,points, category, recurring):
    holder =(name,points,category,recurring)
    conn = get_task_db()
    c = conn.cursor()
    c.execute('insert into tasks (name,points,categories_id, recurring) values(?,?,?,?)',holder)
    conn.commit()

#TODO update task list ( for display in menu )

#update tasks set display = "true" where id=15 <- Statment for changing display val
#test


if __name__ == '__main__':
    #TODO main_menu change to list or tuple 
    main_menu = {
            1:log_tasks_tui,
            2:show_log,
            3:add_task_tui,
            4:add_category_tui
            }

    while True:
        for key in main_menu: 
            print( key, ': ', main_menu[key].__name__)
        choice = input('Select a function: ')
        try: 
            main_menu[int(choice)]()
        except Exception as error:
            print(error)
            break
        
print('exiting')


