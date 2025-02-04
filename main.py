from os import system
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from win10toast import ToastNotifier
from datetime import datetime


import sqlite3
from datetime import datetime
import os
from The_database import *

toaster = ToastNotifier()
Window = Tk()
Window.title("Календарь праздников")
Window.geometry("600x600+0+0")
#Создание главного окна

listbox = Listbox()
listbox.grid(row=1, column=0, columnspan=2)
listbox.place(x=10, y=55)
listbox.place(width=580, height=530)
# создаем список

def limit_length(P):
    if len(P) <= 5:
        return True
    else:
        return False

def today_is(): # получение сегодняшней даты
    day = str(datetime.now().day)
    month = str(datetime.now().month)

    if int(month) < 10:
        month = '0' + month
    if int(day) < 10:
        day = '0' + day
    today_is_the_data = day + "." + month
    return today_is_the_data

def raise_notification(name): # вывод уведомления если сегодня праздник
    try:
        toaster.show_toast("Сегодня праздник!", f'Праздник: {name}', threaded=True,
                    icon_path=None, duration=5)
    except TypeError:
        pass

def notify_check(): # проверка на праздник сегодня
    try:
        data = Selection()
        date, name = data[0]
        if today_is() == date:
            raise_notification(name)
    except IndexError:
        return

notify_check()

list = Selection()
for i, j in enumerate(list):
    listbox.insert(i, j)
    # добавление нового элемента

def delete_listbox(): # очистка поля значений в окне
    listbox.delete(0, 'end')
    list = Selection()
    for i, j in enumerate(list):
        listbox.insert(i, j)

def delete_all(): # удалить всё
    delete()
    listbox.delete(0, 'end')

def delete_ones(flag=False, date=None, name=None): # удалить единичный объект
    try:
        if flag is False:
            selection = listbox.curselection()
            selected = listbox.get(selection[0])
            listbox.delete(selection[0])
        else:
            selected = date, name
    except IndexError:
        return
    delete_selected(selected)


def openNewWindow(): #Создание второстепенного окна
    newWindow = Toplevel(Window)
    newWindow.title("New Window")
    newWindow.geometry("200x150")
    newWindow.resizable(False, False)

    def To_close(): # закрыть мини окошко
        newWindow.destroy()

    def add_to_the_database(): # Добавляет в базу данных
        date = input_data.get()
        holiday = Entering_a_holiday.get()
        result = compare(date, holiday)
        if result is True:
            add(date, holiday)
        elif result is None:
            messagebox.showerror("Ошибка", "Нельзя оставить значение пустым!")
        else:
            messagebox.showerror("Ошибка", "Такое название праздника уже существует!")
        To_close()
        listbox.delete(0, 'end')
        list = Selection()
        for i, j in enumerate(list):
            listbox.insert(i, j)
        
    

    Add = Button(newWindow, text="Добавить", command=add_to_the_database)
    Add.pack(side=TOP)
    Add.place(x=1, y=119)
    Add.place(width=99, height=30)
    #Кнопка "Добавить" в окне "newWindow".


    Cancel = Button(newWindow, text="Отмена", command=To_close)
    Cancel.pack(side=TOP)
    Cancel.place(x=100, y=119)
    Cancel.place(width=99, height=30)
    #Кнопка "Отмена" в окне "newWindow". Закрывает окно.

    data = Label(newWindow, text="Дата:")
    data.place(x=5, y=10)
    #Текст перед вводом

    vcmd = (newWindow.register(limit_length), '%P')
    input_data = Entry(newWindow, validate='key', validatecommand=vcmd)
    input_data.place(x=5, y=30)
    input_data.place(width=190, height=20)
    #Ввод даты

    holiday = Label(newWindow, text="Праздник:")
    holiday.place(x=5, y=60)
    #Текст перед вводом

    Entering_a_holiday = Entry(newWindow)
    Entering_a_holiday.place(x=5, y=80)
    Entering_a_holiday.place(width=190, height=20)
    #Ввод праздника


def new_window_for_changes(): # добавление окна для извенения значений
    newchanges = Toplevel(Window)
    newchanges.title("New Window")
    newchanges.geometry("200x150")
    newchanges.resizable(False, False)


    def close(): # закрыть мини окошко
        newchanges.destroy()

    def make_changes(): # выделение объекта
        try:
            selection = listbox.curselection()
            selected = listbox.get(selection[0])
            listbox.delete(selection[0])
        except IndexError:
            return
        return selected
    
    try:
        result = make_changes() # получение значений
        dateget, nameget = result
    except TypeError:
        pass

    def add_to_the_database(): # Добавляет в базу данных
        date = input_data.get()
        holiday = Entering_a_holiday.get()
        add(date, holiday)
        close()
        delete_ones(True, dateget, nameget)
        listbox.delete(0, 'end')
        list = Selection()
        for i, j in enumerate(list):
            listbox.insert(i, j)
        
    
    changes = Button(newchanges, text="Изменить", command=add_to_the_database)
    changes.pack(side=TOP)
    changes.place(x=1, y=119)
    changes.place(width=99, height=30)
    #Кнопка "Изменить" в окне "newchanges".


    Cancel = Button(newchanges, text="Отмена", command=close)
    Cancel.pack(side=TOP)
    Cancel.place(x=100, y=119)
    Cancel.place(width=99, height=30)
    #Кнопка "Отмена" в окне "newchanges". Закрывает окно.

    data = Label(newchanges, text="Дата:")
    data.place(x=5, y=10)
    #Текст перед вводом

    vcmd = (newchanges.register(limit_length), '%P')
    input_data = Entry(newchanges, validate='key', validatecommand=vcmd)
    input_data.place(x=5, y=30)
    input_data.place(width=190, height=20)
    input_data.insert(0, dateget)
    #Ввод даты

    holiday = Label(newchanges, text="Праздник:")
    holiday.place(x=5, y=60)
    #Текст перед вводом

    Entering_a_holiday = Entry(newchanges)
    Entering_a_holiday.place(x=5, y=80)
    Entering_a_holiday.place(width=190, height=20)
    Entering_a_holiday.insert(0, nameget)
    #Ввод праздника
    

Add = Button(Window, text="Добавить", command=openNewWindow)
Add.pack(side=TOP)
Add.place(x=0, y=0)
Add.place(width=150, height=50)
#Кнопка "Добавить" в главном окне. Открывает окно по добавлению праздника.

Delete_everything = Button(Window, text="Удалить всё", command=delete_all)
Delete_everything.pack(side=TOP)
Delete_everything.place(x=150, y=0)
Delete_everything.place(width=150, height=50)
#Кнопка "Удалить всё" в главном окне. Очищает полностью базу данных.

change = Button(Window, text="Изменить", command=new_window_for_changes)
change.pack(side=TOP)
change.place(x=300, y=0)
change.place(width=150, height=50)
#Кнопка "Изменить" в главном окне. С помощью нее можно изменить определенный праздник.

destroy = Button(Window, text="Удалить", command=delete_ones)
destroy.pack(side=TOP)
destroy.place(x=450, y=0)
destroy.place(width=150, height=50)
#Кнопка "Удалить" в главном окне. С помощью неё можно обновить список праздников.


Window.mainloop()
