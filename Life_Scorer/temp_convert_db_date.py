#Temporary script to convert database schema to new date format.
import interface,datetime,sqlite3

db = interface.get_task_db()
c = db.cursor()
c.execute("SELECT id, timestamp from log")
stamps = c.fetchall()
print(stamps)

time_dict = {}
for stamp in stamps:
    t_id = stamp[0]
    date_time = stamp[1].split(' ')
    date = date_time[0].split('-')
    time = date_time[1].split(':')
    
    year = int(date[0])
    month = int(date[1])
    day = int(date[2])
    
    hour = int(time[0])
    minute = int(time[1])
    second = int(time[2])
    
    dt = datetime.datetime(year,month,day,hour,minute,second)
    #Convert time over from server to local time by subtracting 4 hours
    dt = dt - datetime.timedelta(hours = 4)  
    time_dict[t_id] = dt

conn = sqlite3.connect('test.db')
c = conn.cursor()
c.execute('CREATE TEMPORARY TABLE log_backup(id, task_id, qty, note )')
c.execute('INSERT INTO log_backup SELECT id, task_id, qty, note FROM log')
c.execute('DROP TABLE log')
c.execute('''CREATE TABLE log(
    id integer primary key, 
    task_id integer, 
    qty integer, 
    note text,
    date text,
    time text,
    FOREIGN KEY(task_id) REFERENCES tasks(id)
    )''')
c.execute('INSERT INTO log (id, task_id, qty, note) SELECT id, task_id, qty, note FROM log_backup;')
c.execute('DROP TABLE log_backup')
conn.commit()

for log_id in time_dict:
    date = str(time_dict[log_id].date())
    time = str(time_dict[log_id].time())
    print(date, time, log_id)
    holder = (date, time, log_id)
    c.execute("update log set date = ?, time = ? where id = ?",holder)

conn.commit()

'''
CREATE TEMPORARY TABLE t1_backup(a,b);
INSERT INTO t1_backup SELECT a,b FROM t1;
DROP TABLE t1;
CREATE TABLE t1(a,b);
INSERT INTO t1 SELECT a,b FROM t1_backup;
DROP TABLE t1_backup;
COMMIT;
'''