#average an attribute from db file
#as written is hardcoded 
import sqlite3, json, subprocess
path = subprocess.check_output(['./get_latest_db_path.sh'])
path =str(path)
path= path[2:len(path)-3]+'/Rob.db'
conn = sqlite3.connect(path)
cur = conn.cursor()
cur.execute('Select attributes from log where task_id = 14')
r = cur.fetchall()

weights=[]
for i in range(len(r)):
    w=json.loads(r[i][0])
    w=w['qty']
    weights.append(w)

print(sum(weights)/len(weights))
