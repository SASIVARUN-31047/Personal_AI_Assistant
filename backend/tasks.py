import sqlite3

DB = "database.db"

def init_db():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS tasks (task TEXT)")
    con.commit()
    con.close()

def add_task(task):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("INSERT INTO tasks VALUES (?)", (task,))
    con.commit()
    con.close()

def get_tasks():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("SELECT task FROM tasks")
    tasks = [row[0] for row in cur.fetchall()]
    con.close()
    return tasks

def clear_tasks():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("DELETE FROM tasks")
    con.commit()
    con.close()
