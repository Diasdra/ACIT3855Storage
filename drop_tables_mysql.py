import mysql.connector
db_conn = mysql.connector.connect(host="acit3855-jennie-wu-lab6a.eastus.cloudapp.azure.com", user="user",
password="password", database="events")

db_cursor = db_conn.cursor()
db_cursor.execute('''
DROP TABLE rented_car, returned_car
''')

db_conn.commit()
db_conn.close()