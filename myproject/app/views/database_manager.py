import sqlite3 as sql
import os

from datetime import datetime

## database manager ##
# has functions about sql queries
# insert, select query is available
# also initializes db if needed

## warning ##
## every arguments should be filtered
## before entering this file
## no filtering in here...

DATABASE_PATH = "./cykor.db"

def insert_db(table, value):

    # insert into table value
    # automatically check
    # the number of parameters
    
    db = sql.connect(DATABASE_PATH)
    cur = db.cursor()

    columns = "?," * (len(value)-1) + "?"
    cur.execute(f"INSERT INTO {table} VALUES ({columns});", value)
    db.commit()
    db.close()

def select_all_db(table):

    # select * from table
    # return table in type of list

    db = sql.connect(DATABASE_PATH)
    cur = db.cursor()
    cur.execute(f"SELECT * FROM {table}")
    valueList = []
    for row in cur:valueList.append(row)

    db.close()
    return valueList

def delete_post_db(value):

    db = sql.connect(DATABASE_PATH)
    cur = db.cursor()

    queryString = "DELETE FROM POST WHERE USERNAME=? AND TIME=?"
    cur.execute(queryString, value)

    db.commit()
    db.close()

def update_post_db(value):

    db = sql.connect(DATABASE_PATH)
    cur = db.cursor()

    queryString = "UPDATE POST SET TITLE=?,TIME=?,CONTENT=? "
    queryString += "WHERE USERNAME=? AND TIME=?"
    cur.execute(queryString, value)

    db.commit()
    db.close()


def _initialize_db():

    # this function runs only for the first time
    # to create and/or to initialize the database
    # I should've added id but it is too late...
    
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

    ## inserting initial values
    ## should be removed after debugging process
    
    time = str(datetime.now())
    cur.execute("INSERT INTO USER VALUES ('admin', 'admin', 'asdf');")
    cur.execute(f"INSERT INTO POST VALUES ('admin', 'test title', '{time}', 'test content');")
    
    db.commit()
    db.close()
    return 0

