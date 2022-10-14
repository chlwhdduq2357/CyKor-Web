import sqlite3 as sql
import os

from datetime import datetime

## database manager ##
# has functions about sql queries
# insert, select query is available
# also initializes db if needed

## every arguments should be filtered
## before entering this file
## no filtering in here...

DATABASE_PATH = "./cykor.db"

def insert_db(table, value):

    db = sql.connect(DATABASE_PATH)
    cur = db.cursor()

    columns = "?," * (len(value)-1) + "?"
    cur.execute(f"INSERT INTO {table} VALUES ({columns});", value)
    db.commit()
    db.close()

def select_all_db(table):

    db = sql.connect(DATABASE_PATH)
    cur = db.cursor()
    cur.execute(f"SELECT * FROM {table}")
    valueList = []
    for row in cur:valueList.append(row)

    db.close()
    return valueList


def _initialize_db():

    # this function runs only for the first time
    # to create and/or to initialize the database
    
    ##### database configuration #####
    # +------------------------------+
    # | table 1. USER                |
    # +----------+-------------------+
    # | USERID   | id of a user      |
    # +----------+-------------------+   
    # | USERNAME | name of a user    |
    # +----------+-------------------+
    # | PASSWORD | encrypted         |
    # +----------+-------------------+
    # +------------------------------+
    # | table 2. POST                |
    # +----------+-------------------+
    # | USERNAME | name of an author |
    # +----------+-------------------+
    # | TITLE    | title of a post   |
    # +----------+-------------------+
    # | TIME     | time created      |
    # +----------+-------------------+
    # | CONTENT  | content of a post |
    # +----------+-------------------+

    DATABASE_PATH_ABS = os.path.dirname(os.getcwd()) + "\\cykor.db"
    db = sql.connect(DATABASE_PATH_ABS)

    cur  = db.cursor()
    try:
        cur.execute("""CREATE TABLE USER(
                        USERID text NOT NULL,
                        USERNAME text NOT NULL,
                        PASSWORD text NOT NULL
                        );""")
        
        cur.execute("""CREATE TABLE POST(
                        USERNAME text NOT NULL,
                        TITLE text NOT NULL,
                        TIME text NOT NULL,
                        CONTENT text NOT NULL
                        );""")
    except:
        pass
    time = str(datetime.now())
    cur.execute("INSERT INTO USER VALUES ('admin', 'admin', 'asdf');")
    cur.execute(f"INSERT INTO POST VALUES ('admin', 'test title', '{time}', 'test content');")
    
    db.commit()
    db.close()
    return 0

def test():
    db = sql.connect("./test.db")

    cur = db.cursor()
    # cur.execute("CREATE TABLE Test(id INT, name VARCHAR);")

    cur.execute("INSERT INTO Test VALUES (1, 'JACK');")
    cur.execute("INSERT INTO Test VALUES (2, 'BILL');")
    cur.execute("INSERT INTO Test VALUES (3, 'SPAM');")

    cur.execute("SELECT * FROM Test")
    print(cur)
    for row in cur:
        print(row)
    return cur
