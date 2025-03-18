from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from qfluentwidgets import *
from win10toast import ToastNotifier
from datetime import *
from The_database import *
import json

app = QApplication([])
app.setStyle('fusion')

window = FluentWindow()
window.resize(700, 600)
window.setWindowIcon(QIcon('icons8-book-64.png'))
app.setWindowIcon(QIcon('icons8-book-64.png'))
window.setWindowTitle('Happy-Dates')

with open("config/config.json", "r", encoding="utf-8") as cfg:
    data = json.load(cfg)
    setThemeColor(QColor(data["QFluentWidgets"]["ThemeColor"]))
    if data["MainWindow"]["EnableAcrylicBackground"] is True:
        window.setMicaEffectEnabled(True)
    else:
        window.setMicaEffectEnabled(False)

    theme_mode = data["QFluentWidgets"]["ThemeMode"]
    if theme_mode == "Light":
        setTheme(Theme.LIGHT, lazy=True)
    elif theme_mode == "Dark":
        setTheme(Theme.DARK, lazy=True)
    elif theme_mode == "Auto":
        setTheme(Theme.AUTO, lazy=True)
    cfg.close()


home_page = QWidget(window)
home_page.setObjectName('home_page')

add_page = QWidget(window)
add_page.setObjectName('add_page')

change_page = QWidget(window)
change_page.setObjectName('change_page')

delete_page = QWidget(window)
delete_page.setObjectName('delete_page')

search_page = QWidget(window)
search_page.setObjectName('search_page')

settings_page = QWidget(window)
settings_page.setObjectName('settings_page')


window.addSubInterface(home_page, FluentIcon.HOME, 'Главная', NavigationItemPosition.TOP)
window.addSubInterface(add_page, FluentIcon.ADD, 'Добавить', NavigationItemPosition.SCROLL)
window.addSubInterface(change_page, FluentIcon.EDIT, 'Редактировать', NavigationItemPosition.SCROLL)
window.addSubInterface(delete_page, FluentIcon.DELETE, 'Удалить', NavigationItemPosition.SCROLL)
window.addSubInterface(search_page, FluentIcon.SEARCH, 'Поиск', NavigationItemPosition.SCROLL)
window.addSubInterface(settings_page, FluentIcon.SETTING, 'Настройки', NavigationItemPosition.BOTTOM)


main_search_page_layout = QVBoxLayout(search_page)

search_page_heading = TitleLabel(parent=search_page, text='Поиск')


def search_table(string, output_table):
    if string == '':
        update_everything()
        return
    output_table.clear()
    output_table.setHorizontalHeaderLabels(["Наименование", "Дата", "Тип", "Создано"])
    data_base = Selection()
    id_container = []
    for string_id, name, date, type, created in data_base:
        compare_string = ''
        for i in name:
            compare_string += str(i)
            if compare_string.lower() == string.lower():
                id_container.append(string_id)
    output_table.setRowCount(len(id_container))
    for i in range(len(id_container)):
        for string_id, name, date, type, created in data_base:
            if string_id == id_container[i]:
                output_table.setItem(i, 0, QTableWidgetItem(name))
                output_table.setItem(i, 1, QTableWidgetItem(date))
                output_table.setItem(i, 2, QTableWidgetItem(type))
                output_table.setItem(i, 3, QTableWidgetItem(created))


search_entry = SearchLineEdit(search_page)
search_entry.textChanged.connect(lambda text: search_table(text, search_page_table))

search_page_table = TableWidget(search_page)
search_page_table.setColumnCount(4)
search_page_table.setHorizontalHeaderLabels(["Наименование", "Дата", "Тип", "Создано"])
search_page_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
search_page_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

def TableWidget_output():
    search_page_table.setRowCount(0)
    dict = Selection()

    max = search_max()

    search_page_table.setRowCount(max)

    for el in dict:
        search_page_table.setItem(max - el[0], 0, QTableWidgetItem(el[1]))
        search_page_table.setItem(max - el[0], 1, QTableWidgetItem(el[2]))
        search_page_table.setItem(max - el[0], 2, QTableWidgetItem(el[3]))
        search_page_table.setItem(max - el[0], 3, QTableWidgetItem(el[4]))


main_search_page_layout.addWidget(search_page_heading, alignment=Qt.AlignmentFlag.AlignLeft)
main_search_page_layout.addWidget(search_entry, alignment=Qt.AlignmentFlag.AlignCenter)
main_search_page_layout.addWidget(search_page_table, stretch=1)
main_search_page_layout.setContentsMargins(50, 10, 50, 50)
main_search_page_layout.addStretch(1)



settings_page_heading = TitleLabel(parent=settings_page, text='Настройки приложения')

def theme_change(text):
    if text == 'Светлая':
        setTheme(Theme.LIGHT, save=True)
    elif text == 'Тёмная':
        setTheme(Theme.DARK, save=True)
    elif text == 'Системная':
        setTheme(Theme.AUTO, save=True)


personalisation = SubtitleLabel('Персонализация')

theme_card = ExpandGroupSettingCard(
    FluentIcon.BRUSH,
    "Тема приложения",
    "Меняет тему приложения",
    settings_page
)

system_button = RadioButton(text="Системная", parent=settings_page)
light_button = RadioButton(text="Светлая", parent=settings_page)
dark_button = RadioButton(text="Тёмная", parent=settings_page)

system_theme = QButtonGroup(settings_page)
system_theme.addButton(system_button)
system_theme.addButton(light_button)
system_theme.addButton(dark_button)
system_theme.buttonToggled.connect(lambda button: theme_change(button.text()))

if theme_mode == 'Light':
    light_button.setChecked(True)
elif theme_mode == 'Dark':
    dark_button.setChecked(True)
elif theme_mode == 'Auto':
    system_button.setChecked(True)

settings_card_widget = QWidget()
settings_theme_layout = QVBoxLayout(settings_card_widget)
settings_theme_layout.addWidget(system_button)
settings_theme_layout.addWidget(light_button)
settings_theme_layout.addWidget(dark_button)
settings_theme_layout.setContentsMargins(20, 20, 20, 20)

theme_card.addGroupWidget(settings_card_widget)

def main_color_changed(col):
    setThemeColor(QColor(f'{col.name()}'))
    window.update()

main_color_card = ColorSettingCard(
    qconfig.themeColor,
    FluentIcon.PALETTE,
    'Главный цвет',
    'Меняет главный цвет приложения',
    settings_page,
    enableAlpha=False
)
main_color_card.colorChanged.connect(lambda color: main_color_changed(color))

class Config(QConfig):
    enableAcrylicBackground = ConfigItem("MainWindow", "EnableAcrylicBackground", False, BoolValidator())


cfg = Config()
qconfig.load("config/config.json", cfg)

def is_mica_enabled():
    if mica_effect_card.isChecked():
        window.setMicaEffectEnabled(True)
    else:
        window.setMicaEffectEnabled(False)

mica_effect_card = SwitchSettingCard(
    FluentIcon.TRANSPARENT,
    'Эффект Слюды',
    'Добавляет эффект полупрозрачности',
    cfg.enableAcrylicBackground,
    settings_page
)
mica_effect_card.checkedChanged.connect(lambda: is_mica_enabled())

provide_feedback_card = HyperlinkCard(
    'https://github.com/FLOOX143/happy-dates/issues',
    'Оставить отзыв',
    FluentIcon.FEEDBACK,
    'Обратная Связь',
    'Позволяет разработчикам узнать о недоработках',
    settings_page
)

help_documentation_card = PrimaryPushSettingCard(
    'Руководство',
    FluentIcon.INFO,
    'Руководство по пользованию',
    'Помогает разобраться в работе программы',
    settings_page
)

main_settings_page_layout = QVBoxLayout(settings_page)

settings_page_personalisation_widget = QWidget()
settings_page_personalisation_layout = QVBoxLayout(settings_page_personalisation_widget)
settings_page_personalisation_layout.addWidget(personalisation)
settings_page_personalisation_layout.addWidget(mica_effect_card)
settings_page_personalisation_layout.addWidget(theme_card)
settings_page_personalisation_layout.addWidget(main_color_card)
settings_page_personalisation_layout.addStretch(1)

about_label = SubtitleLabel('О программе')
settings_page_about_widget = QWidget()
settings_page_about_layout = QVBoxLayout(settings_page_about_widget)
settings_page_about_layout.addWidget(about_label)
settings_page_about_layout.addWidget(provide_feedback_card)
settings_page_about_layout.addWidget(help_documentation_card)
settings_page_about_layout.addStretch(1)

main_settings_page_layout.addWidget(settings_page_heading)
main_settings_page_layout.addWidget(settings_page_personalisation_widget)
main_settings_page_layout.addWidget(settings_page_about_widget)
main_settings_page_layout.setContentsMargins(50, 10, 50, 50)
main_settings_page_layout.setSpacing(20)
main_settings_page_layout.addStretch(1)



table_widget_add = TableWidget(add_page)
table_widget_add.setGeometry(10, 290, 620, 250)
table_widget_add.setColumnCount(4)
table_widget_add.setHorizontalHeaderLabels(["Наименование", "Дата", "Тип", "Создано"])
table_widget_add.setColumnWidth(0, 230)  
table_widget_add.setColumnWidth(1, 100) 
table_widget_add.setColumnWidth(2, 150)
table_widget_add.setColumnWidth(3, 110)
table_widget_add.setEditTriggers(QTableWidget.NoEditTriggers)
table_widget_add.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)

def search_max():
    dict = Selection()
    max = 0
    for i in dict:
        max += 1
    return max

def TableWidget_ADD1():
    table_widget.setRowCount(0)
    dict = Selection()

    max = search_max()

    table_widget.setRowCount(max)

    for el in dict:
        table_widget.setItem(max - el[0], 0, QTableWidgetItem(el[1]))
        table_widget.setItem(max - el[0], 1, QTableWidgetItem(el[2]))
        table_widget.setItem(max - el[0], 2, QTableWidgetItem(el[3]))
        table_widget.setItem(max - el[0], 3, QTableWidgetItem(el[4]))

def TableWidget_ADD2():
    table_widget_add.setRowCount(0)
    dict = Selection()

    max = search_max()

    table_widget_add.setRowCount(max)

    for el in dict:
        table_widget_add.setItem(max - el[0], 0, QTableWidgetItem(el[1]))
        table_widget_add.setItem(max - el[0], 1, QTableWidgetItem(el[2]))
        table_widget_add.setItem(max - el[0], 2, QTableWidgetItem(el[3]))
        table_widget_add.setItem(max - el[0], 3, QTableWidgetItem(el[4]))


def TableWidget_ADD3():
    table_widget_change.setRowCount(0)
    dict = Selection()

    max = search_max()

    table_widget_change.setRowCount(max)

    for el in dict:
        table_widget_change.setItem(max - el[0], 0, QTableWidgetItem(el[1]))
        table_widget_change.setItem(max - el[0], 1, QTableWidgetItem(el[2]))
        table_widget_change.setItem(max - el[0], 2, QTableWidgetItem(el[3]))
        table_widget_change.setItem(max - el[0], 3, QTableWidgetItem(el[4]))

def TableWidget_ADD4():
    table_widget_delete.setRowCount(0)
    dict = Selection()

    max = search_max()

    table_widget_delete.setRowCount(max)

    for el in dict:
        table_widget_delete.setItem(max - el[0], 0, QTableWidgetItem(el[1]))
        table_widget_delete.setItem(max - el[0], 1, QTableWidgetItem(el[2]))
        table_widget_delete.setItem(max - el[0], 2, QTableWidgetItem(el[3]))
        table_widget_delete.setItem(max - el[0], 3, QTableWidgetItem(el[4]))

def update_everything():
    TableWidget_ADD4()
    TableWidget_ADD3()
    TableWidget_ADD2()
    TableWidget_ADD1()
    TableWidget_output()

def add_The_database():
    Name = line_edit_add_Name.text()
    Date = line_edit_add_Date.text()
    Type = line_edit_add_Type.text()

    if Name != "" and Date != "":
        now = datetime.now()
        Created = now.strftime("%d.%m.%Y %H:%M")
        add(Name, Date, Type, Created)
        line_edit_add_Name.clear()
        line_edit_add_Date.clear()
        update_everything()

button_add = PushButton(parent=add_page, text='Добавить')
button_add.setGeometry(10, 10, 150, 50)
button_add.clicked.connect(add_The_database)

line_edit_add_Name = LineEdit(parent=add_page)
line_edit_add_Name.setGeometry(10, 100, 630, 50)

body_label_add_Name = BodyLabel(parent=add_page, text="Наименование")
body_label_add_Name.setGeometry(20, 60, 550, 50)

line_edit_add_Date = LineEdit(parent=add_page)
line_edit_add_Date.setGeometry(10, 170, 630, 50)

body_label_add_Date = BodyLabel(parent=add_page, text="Дата")
body_label_add_Date.setGeometry(20, 130, 550, 50)

line_edit_add_Type = ComboBox(parent=add_page)
line_edit_add_Type.setGeometry(10, 240, 630, 40)
line_edit_add_Type.addItems(["Семейный", "Профессиональный", "Государственный", "Международный", "Народный", "Религиозный"])

body_label_add_Type = BodyLabel(parent=add_page, text="Тип")
body_label_add_Type.setGeometry(20, 200, 550, 50)



table_widget_change = TableWidget(change_page)
table_widget_change.setGeometry(10, 290, 620, 250)
table_widget_change.setColumnCount(4)
table_widget_change.setHorizontalHeaderLabels(["Наименование", "Дата", "Тип", "Создано"])
table_widget_change.setColumnWidth(0, 230)  
table_widget_change.setColumnWidth(1, 100) 
table_widget_change.setColumnWidth(2, 150)
table_widget_change.setColumnWidth(3, 110)
table_widget_change.setEditTriggers(QTableWidget.NoEditTriggers)
table_widget_change.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)




def receiving_data():
    global row_data
    row_data = []
    row = table_widget_change.currentRow()

    for col in range(0,4):
        item = table_widget_change.item(row, col)
        if item is not None:
            row_data.append(item.text())
    
    Name, Date, Type, Created = row_data
    line_edit_change_Name.setText(Name)
    line_edit_change_Date.setText(Date)
    line_edit_change_Type.setText(Type)


def change_The_database():
    
    Name = line_edit_change_Name.text()
    Date = line_edit_change_Date.text()
    Type = line_edit_change_Type.text()
    
    if Name != "" and Date != "":
        now = datetime.now()
        Created = now.strftime("%d.%m.%Y %H:%M")
        add(Name, Date, Type, Created)
        line_edit_change_Name.clear()
        line_edit_change_Date.clear()
        update_everything()

def delete_choose():
    Name, Date, Type, Created = row_data
    delete_selected(Name, Date, Type, Created)
    update()
    update_everything()



table_widget_change.cellClicked.connect(receiving_data)

button_change = PushButton(parent=change_page, text='Редактировать')
button_change.setGeometry(10, 10, 150, 50)
button_change.clicked.connect(change_The_database)
button_change.clicked.connect(delete_choose)

line_edit_change_Name = LineEdit(parent=change_page)
line_edit_change_Name.setGeometry(10, 100, 630, 50)

body_label_change_Name = BodyLabel(parent=change_page, text="Наименование")
body_label_change_Name.setGeometry(20, 60, 550, 50)

line_edit_change_Date = LineEdit(parent=change_page)
line_edit_change_Date.setGeometry(10, 170, 630, 50)

body_label_change_Date = BodyLabel(parent=change_page, text="Дата")
body_label_change_Date.setGeometry(20, 130, 550, 50)

line_edit_change_Type = ComboBox(parent=change_page)
line_edit_change_Type.setGeometry(10, 240, 630, 40)
line_edit_change_Type.addItems(["Семейный", "Профессиональный", "Государственный", "Международный", "Народный", "Религиозный"])

body_label_change_Type = BodyLabel(parent=change_page, text="Тип")
body_label_change_Type.setGeometry(20, 200, 550, 50)


table_widget_delete = TableWidget(delete_page)
table_widget_delete.setGeometry(10, 70, 620, 460)

table_widget_delete.setRowCount(1)
table_widget_delete.setColumnCount(4)
table_widget_delete.setHorizontalHeaderLabels(["Наименование", "Дата", "Тип", "Создано"])
table_widget_delete.setColumnWidth(0, 230)  
table_widget_delete.setColumnWidth(1, 100) 
table_widget_delete.setColumnWidth(2, 150)
table_widget_delete.setColumnWidth(3, 110)
table_widget_delete.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
table_widget_delete.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)

def receiving_data_table_widget_delete():
    global row_data_2
    row_data_2 = []
    row = table_widget_delete.currentRow()

    for col in range(0,4):
        item = table_widget_delete.item(row, col)
        if item is not None:
            row_data_2.append(item.text())

def delete_choose_table_widget_delete():
    Name, Date, Type, Created = row_data_2
    delete_selected(Name, Date, Type, Created)
    update()

    update_everything()

def delete_table_widget_delete():
    delete()

    update_everything()

table_widget_delete.cellClicked.connect(receiving_data_table_widget_delete)

button_delete1 = PushButton(parent=delete_page, text='Удалить')
button_delete1.setGeometry(10, 10, 150, 50)
button_delete1.clicked.connect(delete_choose_table_widget_delete)

button_delete2 = PushButton(parent=delete_page, text='Удалить всё')
button_delete2.setGeometry(170, 10, 150, 50)
button_delete2.clicked.connect(delete_table_widget_delete)


button_ADD = PushButton(parent=home_page, text='Добавить')
button_ADD.setGeometry(10, 10, 150, 50)
button_ADD.clicked.connect(lambda: window.switchTo(add_page)) 

button_EDIT = PushButton(parent=home_page, text='Редактировать')
button_EDIT.setGeometry(170, 10, 150, 50)
button_EDIT.clicked.connect(lambda: window.switchTo(change_page)) 

button_DELETE = PushButton(parent=home_page, text='Удалить')
button_DELETE.setGeometry(330, 10, 150, 50)
button_DELETE.clicked.connect(lambda: window.switchTo(delete_page)) 

button_SETTING = PushButton(parent=home_page, text='Поиск')
button_SETTING.setGeometry(490, 10, 150, 50)
button_SETTING.clicked.connect(lambda: window.switchTo(search_page)) 


table_widget = TableWidget(home_page)
table_widget.setGeometry(10, 70, 620, 460)
table_widget.setColumnCount(4)
table_widget.setHorizontalHeaderLabels(["Наименование", "Дата", "Тип", "Создано"])
table_widget.setColumnWidth(0, 230)  
table_widget.setColumnWidth(1, 100) 
table_widget.setColumnWidth(2, 150)
table_widget.setColumnWidth(3, 110)
table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)

update_everything()

window.show()
app.exec()