# Title: Python Final Project
# Authors: Dominic Corneliusen and Josiah Bliss
# Date last modified: 5/11/2026
# Date last modified: 5/13/2026

import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
'''
import os
#Is this necessary? Should we add an option to save and an option to open a file?
 
if os.path.exists("students.db"):
    os.remove("students.db")
'''
class Database:
    def __init__(self):
        self.conn = sqlite3.connect("students.db")
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL,
                Age INTEGER,
                Grade INTEGER,
                Gender TEXT,
                GPA REAL,
                Subject TEXT
            )
        """)
        self.conn.commit()

    def add_student(self, Name, Age, Grade, Gender, GPA, Subject):
        self.cursor.execute("""
            INSERT INTO students (Name, Age, Grade, Gender, GPA, Subject)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (Name, Age, Grade, Gender, GPA, Subject))
        self.conn.commit()

    def get_students(self):
        self.cursor.execute("SELECT * FROM students")
        return self.cursor.fetchall()

    def update_student(self, student_ID, Name, Age, Grade, Gender, GPA, Subject):
        self.cursor.execute("""
            UPDATE students
            SET Name=?, Age=?, Grade=?, Gender=?, GPA=?, Subject=?
            WHERE student_ID=?
        """, (Name, Age, Grade, Gender, GPA, Subject, student_ID))
        self.conn.commit()

    def delete_student(self, student_ID):
        self.cursor.execute("DELETE FROM students WHERE student_ID=?", (student_ID,))
        self.conn.commit()


class MyGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Student Database")
        self.db = Database()

        tk.Label(master, text="Student Database", font=("Arial", 14)).pack(pady=10)

        table_frame = tk.Frame(master)
        table_frame.pack()

        columns = ("#", "ID", "Name", "Age", "Grade", "Gender", "GPA", "Subject")

        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

        for col in columns:
            self.tree.heading(col, text=col)
            if col == "#":
                self.tree.column(col, width=40, anchor="center")
            else:
                self.tree.column(col, width=120)

        self.tree.pack(side=tk.LEFT)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        button_frame = tk.Frame(master)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Add Entry", width=15, command=self.add_entry).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Edit Entry", width=15, command=self.edit_entry).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Delete Entry", width=15, command=self.delete_entry).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Refresh", width=15, command=self.refresh).grid(row=0, column=3, padx=5)
        tk.Button(button_frame, text="Quit", width=15, command=master.destroy).grid(row=0, column=4, padx=5)

        self.refresh()

    def get_gender(self, initial="Male"):
        win = tk.Toplevel(self.master)
        win.title("Select Gender")
        win.geometry("250x150")

        gender_var = tk.StringVar(value=initial)

        tk.Label(win, text="Select Gender:").pack(pady=10)
        tk.Radiobutton(win, text="Male", variable=gender_var, value="Male").pack()
        tk.Radiobutton(win, text="Female", variable=gender_var, value="Female").pack()

        result = {"gender": None}

        def submit():
            result["gender"] = gender_var.get()
            win.destroy()

        tk.Button(win, text="OK", width=10, command=submit).pack(pady=10)

        win.grab_set()
        win.wait_window()

        return result["gender"]

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for row in self.db.get_students():
            self.tree.insert("", tk.END, values=row)

    def add_entry(self):
        name = simpledialog.askstring("Add Entry", "Enter name:")
        if not name:
            return

        age = simpledialog.askinteger("Add Entry", "Enter age:")
        if age is None:
            return

        grade = simpledialog.askinteger("Add Entry", "Enter grade:")
        if grade is None:
            return

        gender = self.get_gender()

        gpa = simpledialog.askfloat("Add Entry", "Enter GPA:")
        if gpa is None or not (0 <= gpa <= 4):
            messagebox.showerror("Error", "GPA must be between 0 and 4.")
            return

        subject = simpledialog.askstring("Add Entry", "Enter subject:")
        if not subject:
            return

        self.db.add_student(name, age, grade, gender, gpa, subject)
        self.refresh()
        messagebox.showinfo("Success", "Student added successfully.")

    def edit_entry(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a row to edit.")
            return

        current = self.tree.item(selected[0], "values")
        student_ID = current[0]

        name = simpledialog.askstring("Edit Entry", "Enter new name:", initialvalue=current[1])
        if not name:
            return

        age = simpledialog.askinteger("Edit Entry", "Enter new age:", initialvalue=current[2])
        if age is None:
            return

        grade = simpledialog.askinteger("Edit Entry", "Enter new grade:", initialvalue=current[3])
        if grade is None:
            return

        gender = self.get_gender(initial=current[4])

        gpa = simpledialog.askfloat("Edit Entry", "Enter new GPA:", initialvalue=current[5])
        if gpa is None or not (0 <= gpa <= 4):
            messagebox.showerror("Error", "GPA must be between 0 and 4.")
            return

        subject = simpledialog.askstring("Edit Entry", "Enter new subject:", initialvalue=current[6])
        if not subject:
            return

        self.db.update_student(student_ID, name, age, grade, gender, gpa, subject)
        self.refresh()
        messagebox.showinfo("Success", "Student updated successfully.")

    def delete_entry(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a row to delete.")
            return

        student_ID = self.tree.item(selected[0], "values")[0]

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this student?"):
            self.db.delete_student(student_ID)
            self.refresh()
            messagebox.showinfo("Deleted", "Student deleted successfully.")


root = tk.Tk()
gui = MyGUI(root)
root.mainloop()
