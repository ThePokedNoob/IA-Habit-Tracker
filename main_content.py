import sqlite3
from tkinter import *
from tkinter import ttk

def show_main_page(content_frame, db_path):
    # Connect to the database using a context manager
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        query = """
            SELECT NAME, LEVEL, WATER, WATER_NEEDED_FOR_NEXT_LEVEL
            FROM tree
            WHERE rowid = 1;
        """
        row = cursor.execute(query).fetchone()
        if row:
            treeName, treeLevel, treeWater, treeWaterRequired = row
        else:
            # Set default values or handle the missing row as needed
            treeName, treeLevel, treeWater, treeWaterRequired = "Unknown", "0", "0", "0"

    # Create and configure the main container frame within content_frame
    main_frame = Frame(content_frame)
    main_frame.pack(pady=20)
    
    # "My Tree" label using formatted strings
    lbl_title = Label(main_frame, text=f"{treeName}", font=('Arial', 16, 'bold'))
    lbl_level = Label(main_frame, text=f"Level: {treeLevel}", font=('Arial', 16, 'bold'))
    lbl_water = Label(main_frame, text=f"Water: {treeWater}", font=('Arial', 16, 'bold'))
    lbl_waterRequired = Label(main_frame, text=f"Water needed for next level: {treeWaterRequired}", font=('Arial', 16, 'bold'))
    
    lbl_title.pack(pady=10)
    lbl_level.pack(pady=10)
    lbl_water.pack(pady=10)
    lbl_waterRequired.pack(pady=10)
    
    # Tree image
    tree_image = PhotoImage(file="Tree/tree_stage_6.png")
    lbl_image = Label(main_frame, image=tree_image)
    lbl_image.image = tree_image  # Keep a reference to avoid garbage collection
    lbl_image.pack(pady=10)
    
    # Progress bar
    progress = ttk.Progressbar(main_frame, orient=HORIZONTAL, length=300, mode='determinate')
    progress.pack(pady=10)
    progress['value'] = 60  # Set your initial value here

