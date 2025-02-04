import sqlite3
import sys

data = sqlite3.connect('database.db') # создание базы
c = data.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS holiday (
date text NOT NULL, 
name text NOT NULL
)""")

def add(Date, Name): # добавление в базу
    c.execute('INSERT INTO holiday(date, name) VALUES(?, ?)', (Date, Name))
    data.commit()
    return

def Selection():# выделение всех значений из поля вывода в окне программы
    c.execute("SELECT * FROM holiday")
    cod = c.fetchall()
    return cod

def delete(): # удаление всех значений
    c.execute("DELETE FROM holiday")
    data.commit()

def compare(date, name): # контроль ввода пользователя 
    c.execute('SELECT name FROM holiday WHERE name=?', (name,))
    res = c.fetchall()
    for i in range(len(name)): # проверка на пустое название name
        if name[i] == name[i - 1] and name[i] == ' ':
            name_check = None
        else:
            name_check = True
    for i in range(len(date)): # проверка на пустое название date
        if date[i] == date[i - 1] and date[i] == ' ':
            date_check = None
        else:
            date_check = True
    if name == '' or date == '': # проверка на ввод без символов
        return None
    elif name_check == None or date_check == None:
        return None
    elif res == []: # проверка на существоваение в базе такого же объекта
        return True
    else:
        return False
    
def delete_selected(select): # удалить конкретный(выделенный) объект
    date, name = select
    c.execute('DELETE FROM holiday WHERE date=? AND name=?', (date, name))
    data.commit()
