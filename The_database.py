import sqlite3
import sys

data = sqlite3.connect('database.db')
c = data.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS holiday (
date text NOT NULL, 
name text NOT NULL
)""")

def add(Date, Name):
    c.execute('INSERT INTO holiday(date, name) VALUES(?, ?)', (Date, Name))
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
    count = 0
    for i in range(len(name)):
        if name[i] == name[i - 1] and name[i] == ' ':
            return False
    if name == '' or date == '':
        return None
    elif res == []:
        return True
    else:
        return False
    
def delete_selected(select):
    date, name = select
    c.execute('DELETE FROM holiday WHERE date=? AND name=?', (date, name))
    data.commit()
