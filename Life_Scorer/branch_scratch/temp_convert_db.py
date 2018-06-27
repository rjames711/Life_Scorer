import os, sqlite3

#Checks if file has db extension
#Maybe would be better to use subprocess to call unix file cmd
def is_db_file(file):
    file = file.split('.')
    ext = file[len(file) - 1 ]
    return True if ext == 'db' else False

#Gets the absolute paths of the db files
#TODO check if user.db is in folder in case it gets move to this location at somepoint
def get_db_files():
    print(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(os.path.dirname(os.path.abspath(__file__))) #Change to the run location of script
    os.chdir('../db_files')
    files = os.listdir()
    files = [file for file in files if is_db_file(file)]
    files = [os.path.abspath(file) for file in files]
    return files


def convert_db(db_file_path):
    conn = sqlite3.connect(db_file_path)
    #conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('ALTER TABLE log ADD COLUMN attributes text')
    cursor.execute('UPDATE log SET attributes = "( json here )"')
    test = cursor.execute('SELECT id, qty FROM log')
    test = test.fetchall()
    for record in test:
        id = record[0]
        qty = record[1]
        print('id: ',id,' qty: ', qty)
        json = '{"qty":' + str(qty) + '}'
        conn.execute('UPDATE log SET attributes = ? where id = ?', (json,id))

    conn.commit()
    

#Function to remove column from table
#TODO not working, need to add parameters
def remove_col():
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
    '''
    CREATE TEMPORARY TABLE t1_backup(a,b);
    INSERT INTO t1_backup SELECT a,b FROM t1;
    DROP TABLE t1;
    CREATE TABLE t1(a,b);
    INSERT INTO t1 SELECT a,b FROM t1_backup;
    DROP TABLE t1_backup;
    COMMIT;
    '''


for path in get_db_files():
    convert_db(path)

