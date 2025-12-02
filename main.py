import os
import csv
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

FILENAME = "budget.csv"


def load_data():
    data = []

    if not os.path.exists(FILENAME):
        open(FILENAME, "w").close()
        return data

    with open(FILENAME, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            if len(row) == 3:
                data.append((row[0], int(row[1]), int(row[2])))
    return data


def save_data(data):
    with open(FILENAME, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter=';')
        for m, inc, exp in data:
            writer.writerow([m, inc, exp])


class BudgetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Журнал студентського бюджету")
        self.root.geometry("500x200")

        self.data = load_data()
        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        btn1 = tk.Button(frame, text="Додати місяць", width=35, command=self.add_month)
        btn2 = tk.Button(frame, text="Переглянути історію", width=35, command=self.show_table)
        btn3 = tk.Button(frame, text="Місяць з найбільшими витратами", width=35, command=self.max_expenses)

        btn1.grid(row=0, column=0, pady=5)
        btn2.grid(row=1, column=0, pady=5)
        btn3.grid(row=2, column=0, pady=5)

        self.status = tk.Label(self.root, text="", fg="blue")
        self.status.pack(pady=10)


    def add_month(self):
        month = simpledialog.askstring("Новий місяць", "Місяць:")
        if not month:
            return

        income = simpledialog.askstring("Дохід", "Введіть дохід:")
        expenses = simpledialog.askstring("Витрати", "Введіть витрати:")

        if not (income and expenses and income.isdigit() and expenses.isdigit()):
            messagebox.showerror("Помилка", "Дохід і витрати повинні бути числами.")
            return

        income = int(income)
        expenses = int(expenses)

        self.data.append((month, income, expenses))
        save_data(self.data)

        self.status.config(text=f"Місяць {month} додано!")

    def show_table(self):
        win = tk.Toplevel(self.root)
        win.title("Історія бюджету")
        win.geometry("650x300")

        columns = ["Місяць", "Дохід", "Витрати", "Залишок"]
        table = ttk.Treeview(win, columns=columns, show="headings")

        for col in columns:
            table.heading(col, text=col)
            table.column(col, width=150)

        for month, inc, exp in self.data:
            balance = inc - exp
            table.insert("", tk.END, values=[month, inc, exp, balance])

        table.pack(fill="both", expand=True)

    def max_expenses(self):
        if not self.data:
            messagebox.showerror("Помилка", "Немає даних.")
            return

        worst = max(self.data, key=lambda x: x[2])
        month, income, expenses = worst

        messagebox.showinfo(
            "Максимальні витрати",
            f"Найбільші витрати були у місяці {month}: {expenses} грн"
        )


root = tk.Tk()
app = BudgetApp(root)
root.mainloop()
