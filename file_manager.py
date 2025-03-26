from tkinter import Tk
from tkinter.filedialog import *

def askForDatabase():
    Tk().withdraw()  # Hide the main Tkinter window
    
    # Configure the file dialog to show SQLite database files by default
    filename = askopenfilename(
        title="Select SQLite Database",
        filetypes=[
            ("SQLite databases", "*.sqlite *.sqlite3 *.db *.db3"),
            ("All files", "*.*")
        ]
    )
    print(f"Selected database: {filename}")
    return filename

def askForDatabaseSaveLocation():
    a = askopenfile()
    