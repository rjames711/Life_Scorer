if __name__ == '__main__':
    import interface
else:
    import Life_Scorer.interface as interface
import datetime, sqlite3, json

#Gets the task somes for a particular day  (in format YYYY-MM-DD )
def get_sums_by_day(day,user):
    day_sums = {}
    db = interface.get_task_db(user)
    db.row_factory = sqlite3.Row
    c = db.cursor()
    c.execute('SELECT * FROM log WHERE date =?',(day,))
    day_log = c.fetchall()
    for log in day_log:
        task_id = log['task_id']
        task = interface.get_task(task_id,user)
        taskname = task.name
        attributes = json.loads(log['attributes'])
        for attr in attributes:
            if ( taskname , attr ) in day_sums:
                day_sums[(taskname, attr)] += attributes[attr]
            else:
                day_sums[(taskname, attr)] = attributes[attr]
    return day_sums

#Gets total sums for a list of days [ 'YYYY-MM-DD' , ..... ]
def get_days_sums(days, user):
    days_sums = {}
    for day in days:
        single_day_sums = get_sums_by_day(day, user)
        for task in single_day_sums:
            if task in days_sums:
                days_sums[task]+=single_day_sums[task]
            else:
                days_sums[task] = single_day_sums[task]
    return days_sums



