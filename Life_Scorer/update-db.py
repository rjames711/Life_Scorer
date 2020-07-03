import interface, datetime, sqlite3, os

files = os.listdir('./db_files')
dbs = [x.split('.')[0] for x in files if x.split('.')[1] == 'db']

def add_table():
    for user in dbs:
        db = interface.get_task_db(user)
        db.execute('''CREATE TABLE scripts(
                        id INTEGER PRIMARY KEY,
                        script_name TEXT NOT NULL,
                        script TEXT NOT NULL ); ''')
        db.commit()


def add_column():
    for user in dbs:
        db = interface.get_task_db(user)
        db.execute('ALTER TABLE tasks ADD COLUMN description text')
        db.commit()
    
add_table()

