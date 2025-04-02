import sqlite3
from tkinter import *
from tkinter import ttk
from habits_page import show_habits_page

def show_main_page(content_frame, db_path):
    # Clear existing widgets from the content_frame only
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Connect to the database using a context manager
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        query = """
            SELECT TREE_NAME, LEVEL, WATER, WATER_NEEDED_FOR_NEXT_LEVEL
            FROM tree
            WHERE rowid = 1;
        """
        row = cursor.execute(query).fetchone()
        if row:
            treeName, treeLevel, treeWater, treeWaterRequired = row
        else:
            # Set default values or handle the missing row as needed
            treeName, treeLevel, treeWater, treeWaterRequired = "Unknown", "0", "0", "0"

    # Convert water values to integers (using 0 if conversion fails)
    try:
        water_current = int(treeWater)
    except ValueError:
        water_current = 0
    try:
        water_required = int(treeWaterRequired)
    except ValueError:
        water_required = 0

    # Calculate the percentage for the progress bar.
    # Avoid division by zero.
    progress_percent = 0
    if water_required > 0:
        progress_percent = min(100, (water_current / water_required) * 100)

    # Create and configure the main container frame within content_frame
    main_frame = Frame(content_frame)
    main_frame.pack(pady=20)
    
    # "My Tree" labels using formatted strings
    lbl_title = Label(main_frame, text=f"{treeName}", font=('Arial', 16, 'bold'))
    lbl_level = Label(main_frame, text=f"Level: {treeLevel}", font=('Arial', 16, 'bold'))
    
    lbl_title.pack(pady=10)
    lbl_level.pack(pady=10)
    
    # Tree image
    tree_image = PhotoImage(file="Tree/tree_stage_6.png")
    lbl_image = Label(main_frame, image=tree_image)
    lbl_image.image = tree_image  # Keep a reference to avoid garbage collection
    lbl_image.pack(pady=10)
    
    # Style configuration for the progress bar
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("green.Horizontal.TProgressbar", 
                    troughcolor ='#D3D3D3', 
                    background ='#4CAF50', 
                    thickness=20)
    
    # Progress bar showing the water level progress
    progress = ttk.Progressbar(main_frame, 
                               orient=HORIZONTAL, 
                               length=300, 
                               mode='determinate', 
                               style="green.Horizontal.TProgressbar")
    progress.pack(pady=10)
    progress['value'] = progress_percent

    # Label showing progress text (e.g., "50/100")
    progress_label = Label(main_frame, 
                           text=f"{water_current} / {water_required}", 
                           font=('Arial', 12))
    progress_label.pack(pady=5)
    
    # "View Habits" button
    btn_view_habits = Button(main_frame, text="View Habits", font=('Arial', 12, 'bold'), 
                             bg="#2196F3", fg="white", padx=10, pady=5,
                             relief=RAISED, bd=2, cursor="hand2")
    btn_view_habits.pack(pady=15)
    btn_view_habits.config(command=lambda: show_habits_page(content_frame, db_path))