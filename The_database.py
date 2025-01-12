import sqlite3
import sys

data = sqlite3.connect('database.db')
c = data.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS holiday (
date text NOT NULL, 
name text NOT NULL
)""")

def add(Date, Name):
    Date1 = Date
    Name1 = Name
    c.execute('INSERT INTO holiday(date, name) VALUES(?, ?)', (Date1, Name1))
    data.commit()
    return

def Selection():
    c.execute("SELECT * FROM holiday")
    cod = c.fetchall()
    return cod

def delete():
    c.execute("DELETE FROM holiday")
    data.commit()

def compare(date, name):
    c.execute('SELECT name FROM holiday WHERE name=?', (name,))
    res = c.fetchall()
    if name == '' or date == '':
        return None
    elif res == []:
        return True
    else:
        return False

def delete_selected(select):
    date, name = select
    c.execute('DELETE FROM holiday WHERE name=?', (name,))
    data.commit()
