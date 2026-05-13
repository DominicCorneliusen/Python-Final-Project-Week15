#Title: Python Final Project
#Authors: Dominic Corneliusen and Josiah Bliss
#Date last modified: 5/11/2026

import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('students.db')
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table():
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                Name TEXT,
                Age INTEGER,
                Grade INTEGER,
                Student_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Gender TEXT,
                GPA REAL,
                Subject TEXT
            )
        ''')
        self.conn.commit()
        
    def add_student(self, Name, Age, Grade, Gender, GPA, Subject):
        self.cursor.execute('''
        INSERT INTO students (Name, Age, Grade, Gender, GPA, Subject)
        VALUES (?,?,?,?,?,?)
        ''', (Name, Age, Grade, Gender, GPA, Subject))
        self.conn.commit()

    def get_student(self, Student_ID):
        self.cursor.execute('SELECT * FROM students')
        return self.cursor.fetchall()
    
    def delete_student(self, Student_ID):
        self.cursor.execute('DELETE FROM students WHERE Student_ID = ?', (Student_ID,))
        self.conn.commit()

    def update_student(self, Name, Age, Grade, Student_ID, Gender, GPA):
        self.cursor.execute('''
        UPDATE students
        SET Name = ?, Age = ?, Grade = ?, Gender = ?, GPA = ?, Subject = ?
        WHERE Student_ID = ?
        ''', (Name, Age, Grade, Gender, GPA, Subject, Student_ID))
        self.conn.commit()
        
class MYGUI:
    def __init__(self, window):
        self.window = window
        window.title("Student Database")

        self.db = Database()

        self.tableframe = tk.Frame(window)
        self.tableframe.pack(pady=10)

