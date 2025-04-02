import sqlite3
from file_manager import *
from main_content import *
import os

def createDatabase(content_frame):

    # Open save dialog to choose database path
    db_path = asksaveasfilename(
        defaultextension='.db',
        filetypes=[('Database files', '*.db'), ('All files', '*.*')],
        title='Save Database As',
        initialfile='habit_tree_save_file.db'
    )
    
    # Exit if user canceled the dialog
    if not db_path:
        return
    
    # Delete existing file if it exists (after user confirmed overwrite)
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
        except Exception as e:
            print(f"Error removing existing file: {e}")
            return
    
    try:
        # Connect to the new database
        sqliteConnection = sqlite3.connect(db_path)
        cursor = sqliteConnection.cursor()
        
        # Create table with the current tree
        cursor.execute('''CREATE TABLE tree(
            TREE_NAME TEXT,
            LEVEL INTEGER,
            WATER INTEGER,
            WATER_NEEDED_FOR_NEXT_LEVEL INTEGER);''')

        # Create table with the current habits
        cursor.execute('''CREATE TABLE habits(
            HABIT_NAME TEXT,
            DESCRIPTION TEXT,
            TYPE INTEGER,
            PRIORITY INTEGER);''')
        
        # Insert initial data with correct syntax
        cursor.execute('''INSERT INTO tree VALUES (
            'My Tree',
            1,
            0,
            50)''')
        
        sqliteConnection.commit()
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if sqliteConnection:
            sqliteConnection.close()
    
    # Show main page after creation
    show_main_page(content_frame, db_path)

def importDatabase(content_frame):
    filename = askForDatabase()
    if filename:
        # Add your import logic here
        print(f"Database imported from: {filename}")

        # Show main page after import
        show_main_page(content_frame, filename)