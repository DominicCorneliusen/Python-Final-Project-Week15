# Title: Python Final Project
# Authors: Dominic Corneliusen and Josiah Bliss
# Date last modified: 5/11/2026
# Date last modified: 5/13/2026

import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import os

if os.path.exists("students.db"):
    os.remove("students.db")

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('students.db')
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
            student_ID INTEGER PRIMARY KEY AUTOINCREMENT,
               Name TEXT,
               Age INTEGER,
               Grade INTEGER,
               Gender TEXT,
               GPA REAL,
               subject TEXT
           )
        ''')
        self.conn.commit()


    def add_student(self, Name, Age, Grade, Gender, GPA, subject):
        self.cursor.execute('''
            INSERT INTO students 
            (Name, Age, Grade, Gender, GPA, subject)
            VALUES (?,?,?,?,?,?)
            ''', (Name, Age, Grade, Gender, GPA, subject))
        self.conn.commit()

    def get_student(self):
        self.cursor.execute("SELECT * FROM students")
        return self.cursor.fetchall()

    def update_student(self, student_ID, Name, Age, Grade, Gender, GPA, subject):
        self.cursor.execute('''
            UPDATE students
            SET 
                Name = ?,
                Age = ?, 
                Grade = ?,
                Gender = ?,
                GPA = ?,
                subject = ?
            WHERE student_ID = ?
        ''', (Name, Age, Grade, Gender, GPA, subject, student_ID))
        self.conn.commit()

    def delete_student(self, student_ID):
        self.cursor.execute('''
            DELETE FROM students
            WHERE student_ID = ?
            ''', (student_ID,))
        self.conn.commit()

class MyGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("student Database")
        self.db = Database()

        title_label = tk.Label(master, text="student Database")
        title_label.pack(pady=10)

        table_frame = tk.Frame(master)
        table_frame.pack(pady=10)

        columns = (
            'ID',
            'Name',
            'Age',
            'Grade',
            'Gender',
            'GPA',
            'subject')

        self.tree = ttk.Treeview(
            table_frame,
            columns = columns,
            show = "headings",
            height = 15)

        for column in columns:
            self.tree.heading(column, text=column)
            self.tree.column(column, width=120)
        self.tree.pack(side=tk.LEFT)

        button_frame = tk.Frame(master)
        button_frame.pack(pady=10)

        add_button = tk.Button(
            button_frame,
            text="Add Entry",
            width=15,
            command=self.add_entry)
        add_button.grid(row=0, column=0, padx=5)

        edit_button = tk.Button(
            button_frame,
            text="Edit Entry",
            width=15,
            command=self.edit_entry)
        edit_button.grid(row=0, column=1, padx=5)

        delete_button = tk.Button(
            button_frame,
            text="Delete Entry",
            width=15,
            command=self.delete_entry)
        delete_button.grid(row=0, column=2, padx=5)

        quit_button = tk.Button(
            button_frame,
            text="Quit",
            width=15,
            command=master.destroy)
        quit_button.grid(row=0, column=3, padx=5)

        self.refresh()

        refresh_button = tk.Button(
            button_frame,
            text="Refresh",
            width=15,
            command=self.refresh)
        refresh_button.grid(row=0, column=4, padx=5)


    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for row in self.db.get_student():
            self.tree.insert("", tk.END, values=row)

    def get_gender(self):
        gender_window = tk.Toplevel(self.master)
        gender_window.title("Select Gender")
        gender_window.geometry("250x150")

        gender_var = tk.StringVar(value="Male")

        tk.Label(gender_window,text="Select Gender:").pack(pady=10)

        tk.Radiobutton(gender_window,text="Male",variable=gender_var,value="Male").pack()

        tk.Radiobutton(gender_window,text="Female",variable=gender_var,value="Female").pack()

        result = {"gender": None}

        def submit():
            result["gender"] = gender_var.get()
            gender_window.destroy()

        tk.Button(gender_window,text="OK",width=10,command=submit).pack(pady=10)

        gender_window.grab_set()
        gender_window.wait_window()

        return result["gender"]

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
        if gpa is None:
            return

        subject = simpledialog.askstring("Add Entry", "Enter subject:")
        if not subject:
            return

        if gpa < 0 or gpa > 4:
            messagebox.showerror("Error", "GPA must be between 0 and 4.")
            return

        self.db.add_student(
            name,
            age,
            grade,
            gender,
            gpa,
            subject)

        self.refresh()

        messagebox.showinfo("Success","student added successfully.")

    def edit_entry(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showerror("Error","Please select a row to edit.")
            return

        current_student = self.tree.item(selected[0], "values")

        student_ID = current_student[0]

        name = simpledialog.askstring("Edit Entry","Enter new name:", initialvalue=current_student[1])
        if not name:
            return

        age = simpledialog.askinteger("Edit Entry","Enter new age:", initialvalue=current_student[2])
        if age is None:
            return

        grade = simpledialog.askinteger("Edit Entry","Enter new grade:", initialvalue=current_student[3])
        if grade is None:
            return

        gender = simpledialog.askstring("Edit Entry","Enter new gender:", initialvalue=current_student[4])
        if not gender:
            return

        gpa = simpledialog.askfloat("Edit Entry","Enter new GPA:", initialvalue=current_student[5])
        if gpa is None:
            return

        subject = simpledialog.askstring("Edit Entry","Enter new subject:", initialvalue=current_student[6])
        if not subject:
            return

        if gpa < 0 or gpa > 4:
            messagebox.showerror("Error","GPA must be between 0 and 4.")
            return

        self.db.update_student(
            student_ID,
            name,
            age,
            grade,
            gender,
            gpa,
            subject)

        self.refresh()

        messagebox.showinfo("Success","student updated successfully.")

    def delete_entry(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showerror("Error","Please select a row to delete.")
            return

        current_student = self.tree.item(selected[0], "values")
        student_ID = current_student[0]

        confirm = messagebox.askyesno("Confirm Delete","Are you sure you want to delete this student?")

        if confirm:
            self.db.delete_student(student_ID)
            self.refresh()

            messagebox.showinfo("Deleted","student deleted successfully.")

root = tk.Tk()
gui = MyGUI(root)
root.mainloop()