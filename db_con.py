import sqlite3


def get_db():
    return sqlite3.connect("database.db")

def get_db_instance():
    db = get_db()
    cur = db.cursor()

    return db, cur

if __name__ == '__main__':
    db, cur = get_db_instance()

    #cur.execute("select * from users")
    for r in cur.fetchall():
        print(r)

    cur.execute("create table users ( username varchar(50), data int)")
    db.commit()