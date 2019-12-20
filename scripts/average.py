#average an attribute from db file
#as written is hardcoded and need to be run from same directory as file
import sqlite3
import json
conn = sqlite3.connect('Rob.db')
cur = conn.cursor()
cur.execute('Select attributes from log where task_id = 14')
r = cur.fetchall()

weights=[]
for i in range(len(r)):
    w=json.loads(r[i][0])
    w=w['qty']
    weights.append(w)

print(sum(weights)/len(weights))
