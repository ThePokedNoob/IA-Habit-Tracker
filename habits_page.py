import sqlite3
import tkinter as tk
from tkinter import ttk

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
    habits_window.geometry("500x400")  # Set the window size

    # Define a function to handle window closure which resets the global variable
    def on_close():
        global habits_window
        habits_window.destroy()
        habits_window = None

    # Ensure that closing the window via the window manager triggers our on_close function
    habits_window.protocol("WM_DELETE_WINDOW", on_close)
    
    # Create a container frame in the new window
    container = tk.Frame(habits_window, padx=20, pady=20)
    container.pack(fill="both", expand=True)
    
    # Optionally, connect to the database to fetch habits data.
    habits = []
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            # Adjust the query to match your habits table schema
            query = "SELECT habit_name, habit_frequency FROM habits;"
            habits = cursor.execute(query).fetchall()
    except Exception as e:
        print("Error fetching habits:", e)
    
    # Create a title label for the habits page
    title_label = tk.Label(container, text="Your Habits", font=("Arial", 16, "bold"))
    title_label.pack(pady=10)
    
    # Display the habits if available; otherwise, show a default message.
    if habits:
        for habit in habits:
            habit_name, habit_frequency = habit
            habit_label = tk.Label(container, 
                                   text=f"{habit_name} - Frequency: {habit_frequency}",
                                   font=("Arial", 12))
            habit_label.pack(pady=5)
    else:
        no_habits_label = tk.Label(container, 
                                   text="No habits found.", 
                                   font=("Arial", 12, "italic"))
        no_habits_label.pack(pady=10)
    
    # Button to close the habits window
    close_btn = tk.Button(container, text="Close", font=("Arial", 12, "bold"),
                          bg="#f44336", fg="white", padx=10, pady=5,
                          command=on_close)
    close_btn.pack(pady=15)