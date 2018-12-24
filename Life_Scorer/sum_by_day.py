if __name__ == '__main__':
    import interface
else:
    import Life_Scorer.interface as interface
import datetime, sqlite3, json

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




