import sqlite3
import tkinter as tk
from tkinter import ttk
from add_habit_page import create_add_habit_window

# Global variable to hold the reference to the habits window
habits_window = None

def show_habits_page(content_frame, db_path):
    global habits_window
    
    # Check if the habits window is already open and exists
    if habits_window is not None and tk.Toplevel.winfo_exists(habits_window):
        habits_window.lift()  # Bring the existing window to the front
        return

    # Create a new habits window since one isn't open yet
    habits_window = tk.Toplevel()
    habits_window.title("Habits Page")
    habits_window.geometry("500x800")  # Set the window size

    # Function to handle window closure and reset the global variable
    def on_close():
        global habits_window
        habits_window.destroy()
        habits_window = None

    habits_window.protocol("WM_DELETE_WINDOW", on_close)
    
    # Create a container frame in the new window
    container = tk.Frame(habits_window, padx=20, pady=20)
    container.pack(fill="both", expand=True)
    
    # Title label for the habits page
    title_label = tk.Label(container, text="Your Habits", font=("Arial", 16, "bold"))
    title_label.pack(pady=10)
    
    # Frame for the habits list
    habits_frame = tk.Frame(container)
    habits_frame.pack(fill="both", expand=True)

    # Create a canvas within the habits_frame
    canvas = tk.Canvas(habits_frame)
    canvas.pack(side="left", fill="both", expand=True)
    
    # Add a vertical scrollbar linked to the canvas
    scrollbar = ttk.Scrollbar(habits_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    
    # Create a frame inside the canvas which will hold all habit containers
    scrollable_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    # Function to refresh the habits list
    def refresh_habits():
        # Clear the previous list
        for widget in scrollable_frame.winfo_children():
            widget.destroy()
            
        # Query the database for the latest habits
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                query = "SELECT HABIT_NAME FROM habits;"
                habits = cursor.execute(query).fetchall()
        except Exception as e:
            print("Error fetching habits:", e)
            habits = []

        # Populate the list: each habit is displayed in its own container
        if habits:
            for habit in habits:
                habit_name = habit[0]  # assuming habit is a tuple with one element
                
                # Create a container for each habit with a border
                habit_container = tk.Frame(scrollable_frame, bd=1, relief="solid", padx=5, pady=5)
                habit_container.pack(fill="x", padx=5, pady=5)
                
                habit_label = tk.Label(habit_container, text=habit_name, font=("Arial", 12))
                habit_label.pack(side="left", padx=5, pady=5)
        else:
            no_habits_label = tk.Label(scrollable_frame, text="No habits found.", font=("Arial", 12, "italic"))
            no_habits_label.pack(pady=10)

    # Initial call to display habits
    refresh_habits()

    # Frame to hold the buttons side by side
    buttons_frame = tk.Frame(container)
    buttons_frame.pack(pady=15)
    
    # Button to close the habits window
    close_btn = tk.Button(buttons_frame, text="Close", font=("Arial", 12, "bold"),
                          bg="#f44336", fg="white", padx=10, pady=5,
                          command=on_close)
    close_btn.pack(side="left", padx=5)
    
    # Button to add a new habit; this calls the function from add_habit_page
    add_habit_btn = tk.Button(
        buttons_frame,
        text="Add Habit",
        font=("Arial", 12, "bold"),
        bg="#4CAF50",
        fg="white",
        padx=10,
        pady=5,
        command=lambda: create_add_habit_window(db_path, refresh_habits)
    )
    add_habit_btn.pack(side="left", padx=5)
