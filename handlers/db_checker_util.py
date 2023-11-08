import sqlite3
conn = sqlite3.connect('details.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM details')
data = cursor.fetchall()
conn.close()