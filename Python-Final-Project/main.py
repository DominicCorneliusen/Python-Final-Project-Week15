#Title: Python Final Project
#Authors: Dominic Corneliusen and Josiah Bliss
#Date last modified: 5/13/2026

import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("students.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Students (
                Name TEXT,
                Age INTEGER,
                Grade INTEGER,
                StudentID INTEGER PRIMARY KEY AUTOINCREMENT,
                Gender TEXT,
                GPA REAL,
                Subject TEXT
            )
        """)

        self.conn.commit()

    def get_data(self):
        self.cursor.execute("SELECT * FROM Students")
        return self.cursor.fetchall()

    def delete_data(self, student_id):
        self.cursor.execute("DELETE FROM Students WHERE StudentID = ?", (student_id,))
        self.conn.commit()

class MyGUI:
    def __init__(self, master):
        self.master = master
        master.title("Student Database")

        self.db = Database()

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for row in self.db.get_data():
            self.tree.insert("", tk.END, values=row)

    def add_entry(self):
        Name = simpledialog.askstring("Add Entry", "Name:")
        Age = simpledialog.askinteger("Add Entry", "Age:")
        Grade = simpledialog.askinteger("Add Entry", "Grade:")
        StudentID = simpledialog.askinteger("Add Entry", "Student ID Number:")
        Gender = simpledialog.askstring("Add Entry", "Gender:")
        GPA = simpledialog.askfloat("Add Entry", "GPA:")
        Subject = simpledialog.askstring("Add Entry", "Subject:")

        data_list = [Name, Age, Grade, StudentID, Gender, GPA, Subject]

        self.db.cursor.execute("""
            INSERT INTO Students VALUES (?, ?, ?, ?, ?, ?, ?)
        """, data_list)

        self.db.conn.commit()
        self.refresh()
        messagebox.showinfo("Success", "Entry added.")

    def edit_entry(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a row to edit.")
            return

        old_row = self.tree.item(selected[0], "values")
        old_id = old_row[3]

        New_name = simpledialog.askstring("Edit Entry", "New name:", initialvalue=old_row[0])
        New_age = simpledialog.askinteger("Edit Entry", "New age:", initialvalue=old_row[1])
        New_grade = simpledialog.askinteger("Edit Entry", "New grade:", initialvalue=old_row[2])
        New_studentID = simpledialog.askinteger("Edit Entry", "New ID:", initialvalue=old_row[3])
        New_gender = simpledialog.askstring("Edit Entry", "New gender:", initialvalue=old_row[4])
        New_GPA = simpledialog.askfloat("Edit Entry", "New GPA:", initialvalue=old_row[5])
        New_subject = simpledialog.askstring("Edit Entry", "New subject:", initialvalue=old_row[6])

        self.db.cursor.execute("""
            UPDATE Students
            SET Name=?, Age=?, Grade=?, StudentID=?, Gender=?, GPA=?, Subject=?
            WHERE StudentID=?
        """, (New_name, New_age, New_grade, New_studentID, New_gender, New_GPA, New_subject, old_id))

        self.db.conn.commit()
        self.refresh()
        messagebox.showinfo("Success", "Entry updated.")

    def delete_entry(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a row to delete.")
            return

        row = self.tree.item(selected[0], "values")
        student_id = row[3]

        self.db.delete_data(student_id)
        self.refresh()
        messagebox.showinfo("Deleted", "Entry removed.")


root = tk.Tk()
gui = MyGUI(root)
root.mainloop()
