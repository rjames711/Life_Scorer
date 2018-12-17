import interface, datetime, sqlite3, os

files = os.listdir('./db_files')
dbs = [x.split('.')[0] for x in files if x.split('.')[1] == 'db']

for user in dbs:
    db = interface.get_task_db(user)
    db.execute('ALTER TABLE tasks ADD COLUMN description text')
    db.commit()
    

