import tkinter as tk
from tkinter import ttk
import sqlite3


class Top(tk.Frame):  # основное окно
    def __init__(self, root): 
        super().__init__(root)
        self.init_main()
        self.db = db 
        self.view_records()

    def init_main(self): 
        toolbar = tk.Frame(bg="#AFEEEE", bd=2) # создание панели инструментов
        toolbar.pack(side=tk.TOP, fill=tk.X)
        self.add_img = tk.PhotoImage(file="./img/add.png") # загрузка фото кнопки
        btn_open_dialog = tk.Button(
            toolbar, bg="#ffc0cb", bd=0, image=self.add_img, command=self.open_dialog
        ) # создание кнопки
        btn_open_dialog.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(
            self, columns=("ID", "name", "tel", "email", "salary"), height=45, show="headings"
        )

        # настройка параметров колонок таблицы
        self.tree.column("ID", width=30, anchor=tk.CENTER)
        self.tree.column("name", width=150, anchor=tk.CENTER)
        self.tree.column("tel", width=150, anchor=tk.CENTER)
        self.tree.column("email", width=150, anchor=tk.CENTER)
        self.tree.column("salary", width=150, anchor=tk.CENTER)

        # настройка заголовков колонок таблицы
        self.tree.heading("ID", text="ID")
        self.tree.heading("name", text="ФИО")
        self.tree.heading("tel", text="Телефон")
        self.tree.heading("email", text="Email")
        self.tree.heading("salary", text="Заработная плата")

        self.tree.pack(side=tk.LEFT)

        # загрузка фото и создание ещё кнопок
        self.update_img = tk.PhotoImage(file="./img/update.png")
        btn_edit_dialog = tk.Button(
            toolbar,
            bg="#ffc0cb",
            bd=0,
            image=self.update_img,
            command=self.open_update_dialog,
        )
        btn_edit_dialog.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file="./img/delete.png")
        btn_delete = tk.Button(
            toolbar,
            bg="#ffc0cb",
            bd=0,
            image=self.delete_img,
            command=self.delete_records,
        )
        btn_delete.pack(side=tk.LEFT)

        self.search_img = tk.PhotoImage(file="./img/search.png")
        btn_search = tk.Button(
            toolbar,
            bg="#ffc0cb",
            bd=0,
            image=self.search_img,
            command=self.open_search_dialog,
        )
        btn_search.pack(side=tk.LEFT)

    # открытие диалогового окна для добавления записей
    def open_dialog(self):
        Child()

    #добавление записей в бд
    def records(self, name, tel, email, salary):
        self.db.insert_data(name, tel, email, salary)
        self.view_records()

    # просмотр существующих записей 
    def view_records(self):
        self.db.cursor.execute("SELECT * FROM db")
        [self.tree.delete(i) for i in self.tree.get_children()] # очистка таблицы перед добавлением
        [self.tree.insert("", "end", values=row) for row in self.db.cursor.fetchall()] # добавление записей из бд в таблицу

    # открытие диалогового окна для редактирования записей
    def open_update_dialog(self):
        Update()

    # обновление записей
    def update_records(self, name, tel, email, salary):
        self.db.cursor.execute(
            """UPDATE db SET name=?, tel=?, email=?, salary=? WHERE id=?""",
            (name, tel, email, salary, self.tree.set(self.tree.selection()[0], "#1")),
        )
        self.db.conn.commit()
        self.view_records()

    # удаление записей
    def delete_records(self):
        for selection_items in self.tree.selection():
            self.db.cursor.execute(
                "DELETE FROM db WHERE id=?", (self.tree.set(selection_items, "#1"))
            )
        self.db.conn.commit()
        self.view_records()

    # открытие диалогового окна для поиска записей
    def open_search_dialog(self):
        Search()

    # поиск записей
    def search_records(self, name):
        name = "%" + name + "%"
        self.db.cursor.execute("SELECT * FROM db WHERE name LIKE ?", (name,))

        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert("", "end", values=row) for row in self.db.cursor.fetchall()]

# класс для дочернего окна
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        # настройки окна
        self.title("Добавить сотрудника")
        self.geometry("600x420")
        self.resizable(False, False)
        self.configure(bg='#AFEEEE')

        self.grab_set()
        self.focus_set()

        # метки для полей ввода
        label_name = tk.Label(self, text="ФИО:", bg='#FFC0CB')
        label_name.place(x=50, y=80)
        label_select = tk.Label(self, text="Телефон:", bg='#FFC0CB')
        label_select.place(x=50, y=110)
        label_sum = tk.Label(self, text="E-mail:", bg='#FFC0CB')
        label_sum.place(x=50, y=140)
        label_sal = tk.Label(self, text="Заработная плата:", bg='#FFC0CB')
        label_sal.place(x=50, y=170)

        # поля ввода для данных сотрудника
        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=80)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=110)
        self.entry_tel = ttk.Entry(self)
        self.entry_tel.place(x=200, y=140)
        self.entry_salary = ttk.Entry(self)
        self.entry_salary.place(x=200, y=170)

        # кнопка для закрытия окна
        self.btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy)
        self.btn_cancel.place(x=300, y=330)

        # кнопка для добавления сотрудника
        self.btn_ok = ttk.Button(self, text="Добавить")
        self.btn_ok.place(x=220, y=330)

        # привязка функции при нажатии на кнопку "Добавить"
        self.btn_ok.bind(
            "<Button-1>",
            lambda event: self.view.records(
                self.entry_name.get(), self.entry_email.get(), self.entry_tel.get(), self.entry_salary.get()
            ),
        )

# класс для окна редактирования записи
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    def init_edit(self):
        # настройка окна
        self.title("Изменение данных")
        self.configure(bg='#AFEEEE')

        # кнопка для изменения данных
        btn_edit = ttk.Button(self, text="Изменить")
        btn_edit.place(x=220, y=330)

        # привязка функции при нажатии на кнопку "Изменить"
        btn_edit.bind(
            "<Button-1>",
            lambda event: self.view.update_records(
                self.entry_name.get(), self.entry_email.get(), self.entry_tel.get(), self.entry_salary.get()
            ),
        )
        
        # закрытие окна при нажатии на кнопку "Изменить"
        btn_edit.bind("<Button-1>", lambda event: self.destroy(), add="+")
        self.btn_ok.destroy() # удаление кнопки "Добавить"

    def default_data(self):
        # получение данных выбранной записи
        self.db.cursor.execute(
            "SELECT * FROM db WHERE id=?",
            self.view.tree.set(self.view.tree.selection()[-1], "#1"),
        )

        row = self.db.cursor.fetchone()

        # заполнение полей ввода данными из выбранной записи
        self.entry_name.insert(0, row[1])
        self.entry_email.insert(0, row[2])
        self.entry_tel.insert(0, row[3])
        self.entry_salary.insert(0, row[4])

# класс для окна поиска
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        # настройка окна
        self.title("Поиск по ФИО:")
        self.geometry("300x200")
        self.resizable(False, False)
        self.configure(bg='#ffc0cb')

        # метка для отображения надписи "ФИО:"
        label_search = tk.Label(self, text="ФИО:", bg='#AFEEEE')
        label_search.place(x=50, y=20)

        # поле ввода для поиска
        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=100, y=20, width=150)

        # кнопка для закрытия окна
        btn_cancel = ttk.Button(self, text="Закрыть!", command=self.destroy)
        btn_cancel.place(x=185, y=50)

        # кнопка для выполнения поиска
        search_btn = ttk.Button(self, text="Найти!")
        search_btn.place(x=105, y=50)

        # привязка функции при нажатии на кнопку "Найти"
        search_btn.bind(
            "<Button-1>",
            lambda event: self.view.search_records(self.entry_search.get())
        )

        # закрытие окна при нажатии на кнопку "Найти"
        search_btn.bind("<Button-1>", lambda event: self.destroy(), add="+")


# класс для работы с базой данных
class DB:
    def __init__(self):
        self.conn = sqlite3.connect("db.db")
        self.cursor = self.conn.cursor()

        # создание таблицы, если она не существует
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS db (
                id INTEGER PRIMARY KEY,
                name TEXT,
                tel TEXT,
                email TEXT,
                salary INT
            )"""
        )

        self.conn.commit()
        
    def insert_data(self, name, tel, email, salary):
        # вставка данных в таблицу
        self.cursor.execute(
            """INSERT INTO db (name, tel, email, salary) VALUES(?, ?, ?, ?)""", (name, tel, email, salary)
        )
        
        self.conn.commit()


if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Top(root)
    app.pack()

    # настройки главного окна
    root.title("Список сотрудников компании")
    root.geometry("865x650")
    root['background'] = '#AFEEEE'
    root.resizable(False, False)

    # запуск главного цикла
    root.mainloop()