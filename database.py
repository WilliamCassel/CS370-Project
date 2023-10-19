import sqlite3


def get_db():
    return sqlite3.connect("db.db")

def get_instance():
    db = get_db()
    cur = db.cursor()

    return db, cur

if __name__ == '__main__':
    db, cur = get_instance()

    #cur.execute("select * from users")
    for r in cur.fetchall():
        print(r)

    cur.execute("create table users ( username varchar(50), data int)")
    db.commit()