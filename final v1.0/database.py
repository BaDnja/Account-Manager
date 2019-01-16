import sqlite3
from tkinter import messagebox
import os

def setupDatabase():
    if os.path.exists("files/usersDatabase.db"):
        pass
    else:
        #Open or create DB
        db_conn = sqlite3.connect("files/usersDatabase.db")

        #Create cursor
        #cursor = db_conn.cursor()

        try:
            # Create the table if it doesn't exist
            db_conn.execute(
                "CREATE TABLE IF NOT EXISTS Users(ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,"
                "Name TEXT NOT NULL,Username TEXT NOT NULL, Email TEXT NOT NULL, Password TEXT NOT NULL);")
            #self.cursor.execute("INSERT INTO Users VALUES IF NOT EXISTS (1, 'Name', 'Username', 'Email', 'Password')")

            db_conn.commit()

        except sqlite3.OperationalError:
            messagebox.showerror("Error!", "Table not Created!")