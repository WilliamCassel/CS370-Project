import sqlite3

#setting up the database

#connect to db
def get_db():
    #return sqlite3.connect("database.db")
    return sqlite3.connect("db.sqlite")

#gets db cursor and connection objects
def get_db_instance():
    db = get_db()
    cur = db.cursor()

    return db, cur

if __name__ == '__main__':
    db, cur = get_db_instance()
    #create table with attributes
    cur.execute("create table users ( username varchar(50), email varchar(50), password varchar(50), hb_data real )")
    db.commit()