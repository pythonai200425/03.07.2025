
import sqlite3
import os

# check if file exists
if os.path.exists('db1.db'):
    os.remove('db1.db')  # delete file

# connect to db
# if does not exist -> create + connect
# if does exist -> connect
conn = sqlite3.connect('db1.db')

# allow usage of column name, i.e. row['age']
conn.row_factory = sqlite3.Row  # ...magic ...

# create in memory
# erase after program exit
# conn = sqlite3.connect(':memory:')

cursor = conn.cursor()

# Create table
cursor.execute('''
CREATE TABLE IF NOT EXISTS COMPANY(
    ID INT PRIMARY KEY NOT NULL,
    NAME TEXT NOT NULL default 'unknown',
    AGE INT NOT NULL,
    ADDRESS CHAR(50),
    SALARY REAL
);
''')

#  1
#  unsafe
# cursor.execute('''
# INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY)
# VALUES
#  (1, 'Paul', 32, 'California', 20000.00 ),
#  (2, 'Allen', 25, 'Texas', 15000.00 ),
#  (3, 'Teddy', 23, 'Norway', 20000.00 ),
#  (4, 'Mark', 25, 'Rich-Mond ', 65000.00 ),
#  (5, 'David', 27, 'Texas', 85000.00 ),
#  (6, 'Kim', 22, 'South-Hall', 45000.00 );
# ''')

# 2
# safe - one by one
# cursor.execute('''
# INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY)
# VALUES (?, ?, ?, ?, ?);
# ''', (1, 'Paul', 32, 'California', 20000.00))
# cursor.execute('''
# INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY)
# VALUES (?, ?, ?, ?, ?);
# ''', (2, 'Allen', 25, 'Texas', 15000.00 ))

# 3
# safe - multiple query
data = [
    (1, 'Paul', 32, 'California', 20000.00),
    (2, 'Allen', 25, 'Texas', 15000.00),
    (3, 'Teddy', 23, 'Norway', 20000.00),
    (4, 'Mark', 25, 'Rich-Mond ', 65000.00),
    (5, 'David', 27, 'Texas', 85000.00),
    (6, 'Kim', 22, 'South-Hall', 45000.00),
]
cursor.executemany('''
INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY)
VALUES (?, ?, ?, ?, ?);
''', data)

# unsafe
cursor.execute('''
UPDATE COMPANY SET ADDRESS = 'Texas' WHERE ID = 6;
''')

# targil - change to ?
# **bonus** - change to texas-[current-time] i.e. texas-19:07:00

# solution
# safe
cursor.execute('''
UPDATE COMPANY SET ADDRESS = ? WHERE ID = ?;
''', ('Texas', 6))
# bonus
import datetime
time_now = datetime.datetime.now().strftime('%H:%M:%S')
address_with_time = "Texas " + time_now
cursor.execute('''
UPDATE COMPANY SET ADDRESS = ? WHERE ID = ?;
''', (address_with_time, 6))

cursor.execute('''
DELETE FROM COMPANY WHERE ID = ?
''', (5,))

cursor.execute('''
SELECT * FROM COMPANY;
''')

print('SELECT * FROM COMPANY result=')
result = cursor.fetchall()  # returns list of tuples [(), () ...]

for row in result:
    #          0   1     2    3        4
    # COMPANY (ID, NAME, AGE, ADDRESS, SALARY)
    print(row['name'])

print('SELECT * FROM COMPANY fetchone -> result=')
cursor.execute('''
SELECT * FROM COMPANY;
''')
result = cursor.fetchone()  # returns 1 tuple
print(result['name'])

# input from user:
# 1 input data
# COMPANY (ID, NAME, AGE, ADDRESS, SALARY)
# id , name, age, address, salary
# input and float(input)
# ie id = int(input('enter id:'))
# 2
# run insert
# select * to find and show the new row...
# 3
# run select to present the new row

conn.commit()  # write changes

conn.close()  # close for safety