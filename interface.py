#!/usr/bin/env python3
#TODO alter schema and logic to allow for one time tasks which dissapear when done
#TODO Think of new name for tasks and refactor
#TODO Implement menu by category
#TODO task class 
#TODO In schema, remove change display column to bool and add 'reccurring' column
#TODO Add some functionality for plain notes

import sqlite3

def log_task(task, qty, note):
    holder = (task,qty,note)
    c.execute('insert into log (task_id, qty, note) values(?,?,?)',holder)
    conn.commit()


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


#TODO finish implementing one time task functionality
def add_task_tui():
    c.execute('select * from categories')
    categories = c.fetchall()
    name = input('Enter new task name: ')
    points = input('Enter point value: ')
    print (categories)
    category = input('Select a category: ') 
    displays = ('true','once')
    print('1: Recurring task  2: One Time Task')
    display_type = input('Select task type: ')
    display_type = displays[int(display_type)-1]
    add_task(name,points,category, display_type)


def add_task(name,points, category, display_type):
    holder =(name,points,category,display_type)
    c.execute('insert into tasks (name,points,categories_id, display) values(?,?,?,?)',holder)
    conn.commit()

#TODO update task list ( for display in menu )
#update tasks set display = "true" where id=15 <- Statment for changing display val
#test

conn = sqlite3.connect('test.db')
c = conn.cursor()
c.execute('select id, name from tasks where not display = "false"')
task_list = c.fetchall()
tasks = { k:v for k,v in task_list}
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
conn.commit()
c.close()
conn.close()

