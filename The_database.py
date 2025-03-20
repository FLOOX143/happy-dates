import sqlite3

data = sqlite3.connect('database_new.db') # создание базы
cur = data.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS holiday_calendars (
id INTEGER PRIMARY KEY,
name text NOT NULL,
date text NOT NULL, 
type text NOT NULL,
created text NOT NULL
)""")

def add(Name, Date, Type, Created): # добавление в базу
    cur.execute('INSERT INTO holiday_calendars(name, date, type, created) VALUES(?, ?, ?, ?)', (Name, Date, Type, Created))
    data.commit()
    return

def Selection():# выделение всех значений из поля вывода в окне программы
    cur.execute("SELECT * FROM holiday_calendars")
    cod = cur.fetchall()
    return cod


def delete(): # удаление всех значений
    cur.execute("DELETE FROM holiday_calendars")
    data.commit()

def delete_selected(Name, Date, Type, Created): # удалить конкретный(выделенный) объект
    cur.execute('DELETE FROM holiday_calendars WHERE name = ?  AND date = ? AND type = ? AND created = ?', (Name, Date, Type, Created))
    data.commit()
    
def update():
    cur.execute('SELECT id FROM holiday_calendars ORDER BY id')
    rows = cur.fetchall()

    for index, row in enumerate(rows, start=1):
        cur.execute('UPDATE holiday_calendars SET id = ? WHERE id = ?', (index, row[0]))
    
    data.commit()

print(Selection())
