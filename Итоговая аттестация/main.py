import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import sqlite3

class EmployeeManagementApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Employee Management App")

        self.conn = sqlite3.connect('employees.db')
        self.create_table()

        self.tree = ttk.Treeview(master)
        self.tree["columns"] = ("ID", "Name", "Phone", "Email", "Salary")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="имя")
        self.tree.heading("Phone", text="телефон")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Salary", text="зарплата")
        self.tree.pack(padx=20, pady=20)

        self.create_widgets()
        self.update_treeview()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                phone TEXT,
                email TEXT,
                salary INTEGER
            )
        ''')
        self.conn.commit()

    def create_widgets(self):
        self.add_button = tk.Button(self.master, text="Добавить сотрудника", command=self.add_employee)
        self.add_button.pack(pady=10)
        self.update_button = tk.Button(self.master, text="Обновить сотрудника", command=self.update_employee)
        self.update_button.pack(pady=10)
        self.delete_button = tk.Button(self.master, text="Удалить сотрудника", command=self.delete_employee)
        self.delete_button.pack(pady=10)
        self.search_button = tk.Button(self.master, text="Поиск сотрудника", command=self.search_employee)
        self.search_button.pack(pady=10)
        self.undo_button = tk.Button(self.master, text="Отменить", command=self.undo_action)
        self.undo_button.pack(pady=10)

        # Bind double click event on treeview
        self.tree.bind("<Double-1>", self.on_double_click)

        self.last_action = None  # To store the last action for undo

    def add_employee(self):
        name = simpledialog.askstring("Input", "Введите имя сотрудника:")
        phone = simpledialog.askstring("Input", "Введите телефон сотрудника:")
        email = simpledialog.askstring("Input", "Введите email сотрудника:")
        salary = simpledialog.askinteger("Input", "Введите зарплату сотрудника:")

        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO employees (name, phone, email, salary) VALUES (?, ?, ?, ?)", (name, phone, email, salary))
        self.conn.commit()
        self.update_treeview()
        self.last_action = "add"

    def update_employee(self):
        emp_id = simpledialog.askinteger("Input", "Введите ID сотрудника:")

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM employees WHERE id=?", (emp_id,))
        employee = cursor.fetchone()

        if employee:
            name = simpledialog.askstring("Input", "Введите новое имя сотрудника:", initialvalue=employee[1])
            phone = simpledialog.askstring("Input", "Введите новый телефон сотрудника:", initialvalue=employee[2])
            email = simpledialog.askstring("Input", "Введите новый email сотрудника:", initialvalue=employee[3])
            salary = simpledialog.askinteger("Input", "Введите новую зарплату сотрудника:", initialvalue=employee[4])

            cursor.execute("UPDATE employees SET name=?, phone=?, email=?, salary=? WHERE id=?", (name, phone, email, salary, emp_id))
            self.conn.commit()
            self.update_treeview()
            self.last_action = "update"
        else:
            messagebox.showerror("Error", "Сотрудник не найден.")

    def delete_employee(self):
        emp_id = simpledialog.askinteger("Input", "Введите ID сотрудника:")

        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM employees WHERE id=?", (emp_id,))
        self.conn.commit()
        self.update_treeview()
        self.last_action = "delete"

    def search_employee(self):
        name = simpledialog.askstring("Input", "Введите имя сотрудника:")

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM employees WHERE name=?", (name,))
        employees = cursor.fetchall()

        if employees:
            self.tree.delete(*self.tree.get_children())
            for employee in employees:
                self.tree.insert("", "end", values=employee)
        else:
            messagebox.showinfo("Info", "Сотрудника с таким именем не найдено.")

    def update_treeview(self):
        # Clear the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM employees")
        employees = cursor.fetchall()

        for employee in employees:
            self.tree.insert("", "end", values=employee)

    def on_double_click(self, event):
        item = self.tree.selection()[0]
        employee_id = self.tree.item(item, "values")[0]  # Get the employee ID
        messagebox.showinfo("Employee ID", f"Employee ID: {employee_id}")

    def undo_action(self):
        if self.last_action == "add":
            messagebox.showinfo("Undo", "Отменить действие «Добавить сотрудника»")
            # Implement code to undo the add action
        elif self.last_action == "update":
            messagebox.showinfo("Undo", "Отменить действие «Обновить сотрудника»")
            # Implement code to undo the update action
        elif self.last_action == "delete":
            messagebox.showinfo("Undo", "Отменить действие «Удалить сотрудника»")
            # Implement code to undo the delete action
        else:
            messagebox.showinfo("Undo", "Нет предыдущих действий, которые можно было бы отменить.")

    def on_closing(self):
        self.conn.close()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeManagementApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()