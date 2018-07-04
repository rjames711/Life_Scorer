import os, sqlite3, json

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

#Converts log and tasks table to use a json attributes column based on 
#the qty and points column values respectively.
def convert_db(db_file_path):
    #Convert log table
    print (db_file_path)
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
        json_string = '{"qty":' + str(qty) + '}'
        conn.execute('UPDATE log SET attributes = ? where id = ?', (json_string,id))

    #Convert tasks table
    cursor.execute('ALTER TABLE tasks ADD COLUMN attributes text')
    cursor.execute('UPDATE tasks SET attributes = "( json here )"')
    test = cursor.execute('SELECT id, points FROM tasks')
    test = test.fetchall()
    for record in test:
        id = record[0]
        points = record[1]
        print('id: ',id,' points: ', points)
        #default = { 'attr':{'qty':{"min": 0 , "max":30, "default":10, "scored":1}}, 'unit_points': 10 }
        #default['unit_points'] = points
        default = { 'qty':{"min": 0 , "max":30, "default":10, "scored":1}}
        json_string = json.dumps(default)
        conn.execute('UPDATE tasks SET attributes = ? where id = ?', (json_string,id))

    conn.commit()
    


#Should work unless column has forien key constraint in which may require tweaking
def remove_column(db_path, table, col):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT * FROM '+ table)
    columns = [ d[0] for d in c.description]
    columns.remove(col) #Take out column we want to remove
    columns = str.join(', ', columns) 
    #Building a command manually since I don't know how to do a variable # of ? an
    # since this script won't be exposed to the webapp.
    c.execute('CREATE TEMPORARY TABLE backup ' +'(' +columns+')')
    cmd = 'INSERT INTO backup SELECT ' + columns + ' FROM ' + table
    c.execute(cmd)
    c.execute("SELECT * from sqlite_master where type='table'")
    schemas = c.fetchall()
    print(schemas)

    for schema in schemas:
        if schema[1] == table:
            break
    schema = schema[4:len(schema)]
    schema = schema[0]
    #Remove the column from the schema before recreating
    a = schema.split('\n    ')
    for i in range(len(a)):
        ccol =a[i].split(' ')
        if ccol[0] == col:
            break
    a.pop(i)
    schema = '\n    '.join(a)
    print(schema)
    c.execute('DROP TABLE '+table)
    c.execute(schema)
    cmd = "INSERT INTO " + table+ ' (' + columns +") SELECT " + columns + " FROM backup"
    print(cmd)
    c.execute(cmd)
    conn.commit()
    

for path in get_db_files():
    convert_db(path)
    remove_column(path,'log','qty')
    #remove_column(path,'tasks','points')


