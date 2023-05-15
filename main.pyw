import sqlite3
import create_database
import os


create_database.createAllTables()

con=sqlite3.connect(database=r"ims.db")
cur=con.cursor()

cur.execute("select * from employee")
result=cur.fetchall()

if(len(result)==0):
    os.system("admin.py")
else:
    os.system("login.py")
