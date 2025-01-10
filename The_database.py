import sqlite3
import sys

data = sqlite3.connect('database.db')
c = data.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS holiday (
date text NOT NULL, 
name text NOT NULL,
id INTEGER PRIMARY KEY
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

def delete_selected(select):
    date, name, ident = select
    c.execute('DELETE FROM holiday WHERE id=?', (ident,))
    data.commit()
