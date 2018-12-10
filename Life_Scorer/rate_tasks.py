#!/usr/bin/env python
import datetime,sqlite3
import Life_Scorer.interface as interface

#Returns a list sorted with the most frequent log items first and the most
#infrequent items last
def sort_tasks(history_len, user):
    def get_task_index_by_id(tasks, id):
        for i in range(len(tasks)):
            if tasks[i].task_id == id:
                return i
    task_freq = get_task_freq(history_len, user)
    tasks= interface.read_tasks(user)
    sorted_tasks = []
    for task in task_freq:
        task_id=task[0]
        task_obj = tasks.pop(get_task_index_by_id(tasks , task_id))
        sorted_tasks.append(task_obj)
    return sorted_tasks + tasks

#Gets the frequency of different log items in a given history length
def get_task_freq(history_len, user):
    db = interface.get_task_db(user)
    c = db.cursor()
    c.execute('select * from log order by id desc limit ?',(history_len,))
    a=c.fetchall()
    tasks = {}
    for task in a:
        id = task[1]
        if id not in tasks: 
            tasks[id] = 1
        else: 
            tasks[id]+=1
    return sorted(tasks.items(),key=lambda x: x[1],reverse=True)


