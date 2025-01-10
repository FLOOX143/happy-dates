from os import system
from tkinter import *
from tkinter.ttk import *

import sqlite3
from datetime import datetime
import os
from The_database import *


Window = Tk()
Window.title("Календарь праздников")
Window.geometry("600x600+0+0")
#Создание главного окна

listbox = Listbox()
listbox.grid(row=1, column=0, columnspan=2)
listbox.place(x=10, y=55)
listbox.place(width=580, height=530)
# создаем список


list = Selection()
for i, j in enumerate(list):
    listbox.insert(i, j)
    # добавление нового элемента

def del_list():
    listbox.delete(0, 'end')
    list = Selection()
    for i, j in enumerate(list):
        listbox.insert(i, j)

def delete2():
    delete()
    listbox.delete(0, 'end')

def delete3():
    try:
        selection = listbox.curselection()
        selected = listbox.get(selection[0])
        print(selected)
        listbox.delete(selection[0])
    except IndexError:
        return
    delete_selected(selected)


def openNewWindow():
    newWindow = Toplevel(Window)
    newWindow.title("New Window")
    newWindow.geometry("200x150")
    newWindow.resizable(False, False)

    #Создание второстепенного окна


    def To_close():
        newWindow.destroy()

    def add_to_the_database():
        date = input_data.get()
        holiday = Entering_a_holiday.get()
        add(date, holiday)
        To_close()
        listbox.delete(0, 'end')
        list = Selection()
        for i, j in enumerate(list):
            listbox.insert(i, j)
        #Добавляет в базу данных
    
    

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

    input_data = Entry(newWindow)
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


Add = Button(Window, text="Добавить", command=openNewWindow)
Add.pack(side=TOP)
Add.place(x=0, y=0)
Add.place(width=150, height=50)
#Кнопка "Добавить" в главном окне. Открывает окно по добавлению праздника.

Delete_everything = Button(Window, text="Удалить всё", command=delete2)
Delete_everything.pack(side=TOP)
Delete_everything.place(x=150, y=0)
Delete_everything.place(width=150, height=50)
#Кнопка "Удалить всё" в главном окне. Очищает полностью базу данных.

change = Button(Window, text="Изменить")
change.pack(side=TOP)
change.place(x=300, y=0)
change.place(width=150, height=50)
#Кнопка "Изменить" в главном окне. С помощью нее можно изменить определенный праздник.

destroy = Button(Window, text="Удалить", command=delete3)
destroy.pack(side=TOP)
destroy.place(x=450, y=0)
destroy.place(width=150, height=50)
#Кнопка "Удалить" в главном окне. С помощью неё можно обновить список праздников.


Window.mainloop()
