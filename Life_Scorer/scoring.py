import sqlite3
import datetime
import Life_Scorer.interface as interface

#Takes score in str form YYYY-MM-DD
def get_day_score(day, user):
    conn = interface.get_task_db(user)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('select * from log where date =?',(day,))
    day_activity = c.fetchall()
    score = 0
    for act in day_activity:
        task_id = act['task_id']
        task = interface.get_task(task_id,user)
        try:
            score += float(act['qty']) * float(task.points)
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


