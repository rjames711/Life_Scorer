#!/usr/bin/env python3
#TODO alter schema and logic to allow for one time tasks which dissapear when done
#TODO Think of new name for tasks and refactor
#TODO Implement menu by category

import sqlite3

def log_tasks_tui():
    print()
    for task in tasks: print(task,': ', tasks[task])
    task = input('Select a task: ')
    qty = input('Enter a quantity: ')
    note = input('Enter a note: ')
    confirm = input('Confirm submit task "' + tasks[int(task)] + 
            '" with qty '+qty+ ' (y/n): ' )
    if confirm == 'y':
        log_task(task, qty, note)
        conn.commit()
    else:
        print('canceled')

def show_log():
    c.execute("select tasks.name, log.qty, log.timestamp from tasks inner join log on log.task_id=tasks.id")
    log = c.fetchall()
    print('Qty\tTask')
    print(5*'-'+'\t'+5*'-')
    for i in log: print(i[1],'\t', i[0],'\t',i[2])
    print()

def add_category(name):
    holder =(name,)
    c.execute('insert into categories (name) values(?)',holder)
    conn.commit()

def add_category_tui():
    name = input('Enter new category name: ')
    add_category(name)


def add_task_tui():
    c.execute('select * from categories')
    categories = c.fetchall()
    name = input('Enter new task name: ')
    points = input('Enter point value: ')
    print (categories)
    category = input('Select a category: ') 
    add_task(name,points,category)


def add_task(name,points, category):
    holder =(name,points,category)
    c.execute('insert into tasks (name,points,categories_id) values(?,?,?)',holder)
    conn.commit()

def log_task(task, qty, note):
    holder = (task,qty,note)
    c.execute('insert into log (task_id, qty, note) values(?,?,?)',holder)
    conn.commit()


conn = sqlite3.connect('test.db')
c = conn.cursor()
c.execute('select id, name from tasks')
task_list = c.fetchall()
tasks = { k:v for k,v in task_list}

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
    except:
        break
        
print('exiting')
conn.commit()
c.close()
conn.close()



