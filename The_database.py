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



# def compare(date, name): # контроль ввода пользователя 
#     c.execute('SELECT name FROM holiday WHERE name=?', (name,))
#     res = c.fetchall()
#     for i in range(len(name)): # проверка на пустое название name
#         if name[i] == name[i - 1] and name[i] == ' ':
#             name_check = None
#         else:
#             name_check = True
#     for i in range(len(date)): # проверка на пустое название date
#         if date[i] == date[i - 1] and date[i] == ' ':
#             date_check = None
#         else:
#             date_check = True
#     if name == '' or date == '': # проверка на ввод без символов
#         return None
#     elif name_check == None or date_check == None:
#         return None
#     elif res == []: # проверка на существоваение в базе такого же объекта
#         return True
#     else:
#         return False
