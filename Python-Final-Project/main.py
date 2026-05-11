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

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                Name TEXT,
                Age INTEGER,
                Grade INTEGER,
                Student_ID INTEGER PRIMARY KEY,
                Gender TEXT,
                GPA REAL,
                Subject TEXT,
            )
        ''')

class MYGUI:
    def __init__(self, window):
        self.window = window
        window.title("Student Database")

        self.db = Database()

        self.tableframe = tk.Frame(window)
        self.tableframe.pack(pady=10)

