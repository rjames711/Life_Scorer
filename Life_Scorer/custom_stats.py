import sqlite3
import datetime
import json

try:
    import Life_Scorer.interface as interface
    import Life_Scorer.scoring as scoring
except:
    import interface # For testing as standalone file
    import scoring

#Returns list of scores for all days in log
def get_alltime_day_scores(user):
    conn = interface.get_task_db(user)
    c = conn.cursor()
    c.execute('select date from log')
    d = c.fetchall()
    dates = [ x[0] for x in d]
    dates = list(set(dates))
    data =  []
    for day in dates:
        data.append((scoring.get_day_score(day,user),day))
    data.sort(key=lambda x: x[1],reverse=True)
    return data

#Returns user history in the weekly total scores
#TODO write less obnoxiously
def get_weekly_scores(user):
    a = get_alltime_day_scores(user)
    w = [7*(x+1) for x in range(len(a)//7)]
    b = [(sum(x[0] for x in a[x-7:x]),a[x-7][1]) for x in w]
    b.sort(key=lambda x: x[1], reverse=True)
    return b

def get_monthly_scores(user):
    a = get_alltime_day_scores(user)
    w = [30*(x+1) for x in range(len(a)//30)]
    b = [(sum(x[0] for x in a[x-30:x]),a[x-30][1]) for x in w]
    b.sort(key=lambda x: x[1], reverse=True)
    return b
