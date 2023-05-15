import sqlite3



#==============================================================================
def create_db_1():
    con=sqlite3.connect(database=r"ims.db")
    cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS employee (eid INTEGER PRIMARY KEY AUTOINCREMENT,name text,email text,gender text,contact INTEGER,dob REAL,doj REAL,pass text,utype text,address text,salary INTEGER)")
    con.commit()

#====================================================================
def create_db_2():
    con=sqlite3.connect(database=r"ims.db")
    cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS category (cid INTEGER PRIMARY KEY AUTOINCREMENT,name text)")
    con.commit()

#=========================================================================

def create_db_3():
    con=sqlite3.connect(database=r"ims.db")
    cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS product (pid INTEGER PRIMARY KEY AUTOINCREMENT,category text,supplier text,name text,price REAL,qty INTEGER,status text)")
    con.commit()

#==========================================================

def create_db_4():
    con=sqlite3.connect(database=r"ims.db")
    cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS supplier (sup_id INTEGER PRIMARY KEY AUTOINCREMENT,invoice_no INTEGER,name text,contact INTEGER,address text)")
    con.commit()

#==========================================================

def create_db_5():
    con=sqlite3.connect(database=r"ims.db")
    cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS sales (invoice_no INTEGER PRIMARY KEY AUTOINCREMENT,bill_data text)")
    con.commit()


# ===============================================================================================
# ===============================================================================================
# ===============================================================================================
# ===============================================================================================


# calling all the function

def createAllTables():

    create_db_1()
    create_db_2()
    create_db_3()
    create_db_4()
    create_db_5()

createAllTables()           # Creating all the tables
