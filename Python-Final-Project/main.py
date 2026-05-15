# Title: Python Final Project
# Authors: Dominic Corneliusen and Josiah Bliss
# Date last modified: 5/11/2026
# Date last modified: 5/13/2026
# Date last modified: 5/14/2026

import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk, filedialog
import random
import os

class Database:
    def __init__(self):
        if os.path.exists("students.db"):
            os.remove("students.db")

        self.conn = sqlite3.connect("students.db")
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_ID INTEGER PRIMARY KEY,
                Name TEXT NOT NULL,
                Age INTEGER,
                Grade INTEGER,
                Gender TEXT,
                GPA REAL,
                Advisor TEXT
            )
        """)
        self.conn.commit()

    def generate_unique_id(self):
        while True:
            new_id = random.randint(1000, 9999)
            self.cursor.execute("SELECT 1 FROM students WHERE student_ID=?", (new_id,))
            if not self.cursor.fetchone():
                return new_id

    def add_student(self, student_ID, Name, Age, Grade, Gender, GPA, Advisor):
        self.cursor.execute("""
            INSERT INTO students (student_ID, Name, Age, Grade, Gender, GPA, Advisor)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (student_ID, Name, Age, Grade, Gender, GPA, Advisor))
        self.conn.commit()

    def get_students(self):
        self.cursor.execute("SELECT * FROM students")
        return self.cursor.fetchall()

    def update_student(self, student_ID, Name, Age, Grade, Gender, GPA, Advisor):
        self.cursor.execute("""
            UPDATE students
            SET Name=?, Age=?, Grade=?, Gender=?, GPA=?, Advisor=?
            WHERE student_ID=?
        """, (Name, Age, Grade, Gender, GPA, Advisor, student_ID))
        self.conn.commit()

    def delete_student(self, student_ID):
        self.cursor.execute("DELETE FROM students WHERE student_ID=?", (student_ID,))
        self.conn.commit()

    def export_to(self, filename):
        conn2 = sqlite3.connect(filename)
        cur2 = conn2.cursor()
        cur2.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_ID INTEGER PRIMARY KEY,
                Name TEXT NOT NULL,
                Age INTEGER,
                Grade INTEGER,
                Gender TEXT,
                GPA REAL,
                Advisor TEXT
            )
        """)
        conn2.commit()
        cur2.execute("DELETE FROM students")
        conn2.commit()
        for row in self.get_students():
            cur2.execute("""
                INSERT INTO students (student_ID, Name, Age, Grade, Gender, GPA, Advisor)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, row)
        conn2.commit()
        conn2.close()

    def import_from(self, filename):
        conn2 = sqlite3.connect(filename)
        cur2 = conn2.cursor()
        cur2.execute("SELECT * FROM students")
        rows = cur2.fetchall()
        conn2.close()
        self.cursor.execute("DELETE FROM students")
        self.conn.commit()
        for row in rows:
            self.cursor.execute("""
                INSERT INTO students (student_ID, Name, Age, Grade, Gender, GPA, Advisor)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, row)
        self.conn.commit()


class MyGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Student Database")
        self.db = Database()

        tk.Label(master, text="Student Database", font=("Arial", 14)).pack(pady=10)

        table_frame = tk.Frame(master)
        table_frame.pack()

        columns = ("#", "ID", "Name", "Age", "Grade", "Gender", "GPA", "Advisor")

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
        tk.Button(button_frame, text="Save As...", width=15, command=self.save_as).grid(row=0, column=4, padx=5)
        tk.Button(button_frame, text="Import DB", width=15, command=self.import_db).grid(row=0, column=5, padx=5)
        tk.Button(button_frame, text="Quit", width=15, command=master.destroy).grid(row=0, column=6, padx=5)

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

        students = self.db.get_students()
        for index, row in enumerate(students, start=1):
            numbered_row = (index,) + row
            self.tree.insert("", tk.END, values=numbered_row)

    def add_entry(self):
        name = simpledialog.askstring("Add Entry", "Enter name:", parent=self.master)
        if not name:
            return

        age = simpledialog.askinteger("Add Entry", "Enter age:", parent=self.master)
        if age is None:
            return

        grade = simpledialog.askinteger("Add Entry", "Enter grade:", parent=self.master)
        if grade is None:
            return

        gender = self.get_gender()

        gpa = simpledialog.askfloat("Add Entry", "Enter GPA:", parent=self.master)
        if gpa is None or not (0 <= gpa <= 4):
            messagebox.showerror("Error", "GPA must be between 0 and 4.")
            return

        Advisor = simpledialog.askstring("Add Entry", "Enter Advisor Last Name:", parent=self.master)
        if not Advisor:
            return

        student_ID = self.db.generate_unique_id()

        self.db.add_student(student_ID, name, age, grade, gender, gpa, Advisor)
        self.refresh()
        messagebox.showinfo("Success", f"Student added successfully.\nAssigned ID: {student_ID}")

    def edit_entry(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a row to edit.")
            return

        current = self.tree.item(selected[0], "values")
        student_ID = current[1]

        name = simpledialog.askstring("Edit Entry", "Enter new name:", initialvalue=current[2], parent=self.master)
        if not name:
            return

        age = simpledialog.askinteger("Edit Entry", "Enter new age:", initialvalue=current[3], parent=self.master)
        if age is None:
            return

        grade = simpledialog.askinteger("Edit Entry", "Enter new grade:", initialvalue=current[4], parent=self.master)
        if grade is None:
            return

        gender = self.get_gender(initial=current[5])

        gpa = simpledialog.askfloat("Edit Entry", "Enter new GPA:", initialvalue=current[6], parent=self.master)
        if gpa is None or not (0 <= gpa <= 4):
            messagebox.showerror("Error", "GPA must be between 0 and 4.")
            return

        Advisor = simpledialog.askstring("Edit Entry", "Enter new advisor:", initialvalue=current[7], parent=self.master)
        if not Advisor:
            return

        self.db.update_student(student_ID, name, age, grade, gender, gpa, Advisor)
        self.refresh()
        messagebox.showinfo("Success", "Student updated successfully.")

    def delete_entry(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a row to delete.")
            return

        student_ID = self.tree.item(selected[0], "values")[1]

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this student?"):
            self.db.delete_student(student_ID)
            self.refresh()
            messagebox.showinfo("Deleted", "Student deleted successfully.")

    def save_as(self):
        filename = filedialog.asksaveasfilename(defaultextension=".db", filetypes=[("Database Files", "*.db")])
        if filename:
            self.db.export_to(filename)
            messagebox.showinfo("Saved", "Database exported successfully.")

    def import_db(self):
        filename = filedialog.askopenfilename(filetypes=[("Database Files", "*.db")])
        if filename:
            self.db.import_from(filename)
            self.refresh()
            messagebox.showinfo("Imported", "Database imported successfully.")


root = tk.Tk()
gui = MyGUI(root)
root.mainloop()
