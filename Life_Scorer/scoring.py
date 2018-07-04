import sqlite3
import datetime
import Life_Scorer.interface as interface
#import interface # For testing as standalone file
import json

def score_entry(task, log):
    print('in scoring ',task, log)
    unit_qty = 1
    attributes = task.attributes
    #entry = json.loads(log['attributes'])
    for attr in log:
        if attributes[attr]['scored'] == 1:
            unit_qty *= log[attr]
    return task.points * unit_qty
            


#Takes score in str form YYYY-MM-DD
def get_day_score(day, user):
    conn = interface.get_task_db(user)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('select * from log where date =?',(day,))
    day_activity = c.fetchall()
    score = 0
    for log in day_activity:
        task_id = log['task_id']
        task = interface.get_task(task_id,user)
        log = json.loads(log['attributes'])
        try:
            score += score_entry(task, log)
        except Exception as e:
            print("type error: " + str(e))
    return round(score)

def get_month_scores(user):
    #TODO fix timezone hardcoding below
    dt = datetime.datetime.utcnow() -datetime.timedelta(hours=4)
    scores = []
    for days in range(30):
        offdt = dt - datetime.timedelta(days = days)
        date = str(offdt.date())
        score = get_day_score(date, user)
        scores.append((date, score))
    return scores



