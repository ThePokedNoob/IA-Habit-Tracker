import sqlite3
import tkinter as tk

# Simple tooltip class for Tkinter widgets
class CreateToolTip(object):
    def __init__(self, widget, text='widget info'):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        widget.bind("<Enter>", self.enter)
        widget.bind("<Leave>", self.leave)

    def enter(self, event=None):
        self.showtip()

    def leave(self, event=None):
        self.hidetip()

    def showtip(self):
        if self.tipwindow or not self.text:
            return
        # Calculate the tooltip position
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + cy + self.widget.winfo_rooty() + 25
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)  # Remove window decorations
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("Arial", "10", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def add_habit(habit_entry, habit_type_var, priority_slider, day_vars, add_window, db_path, refresh_callback=None):
    habit_name = habit_entry.get()
    habit_type = habit_type_var.get()  # "good" or "bad"
    priority = priority_slider.get()   # priority value from the slider

    # Gather the selected days into a list
    selected_days = [day for day, var in day_vars.items() if var.get()]
    if habit_name:
        try:
            # Connect to the database and insert habit with its type, priority, and days (as comma-separated string)
            with sqlite3.connect(db_path) as sqliteConnection:
                cursor = sqliteConnection.cursor()
                # Here we assume the habits table has columns: habit name, habit type, priority, water reward, and days.
                cursor.execute('''INSERT INTO habits VALUES (?, ?, ?, 50, ?)''', 
                               (habit_name, habit_type, priority, ",".join(selected_days)))
                sqliteConnection.commit()
        except Exception as e:
            print("Error adding habit:", e)
        finally:
            add_window.destroy()
            if refresh_callback:
                refresh_callback()

def create_add_habit_window(db_path, refresh_callback=None):
    add_window = tk.Toplevel()
    add_window.title("Add New Habit")
    add_window.geometry("450x450")  # Increased height to accommodate day selection

    # Habit name input
    label = tk.Label(add_window, text="Enter new habit name:", font=("Arial", 12))
    label.pack(pady=10)
    habit_entry = tk.Entry(add_window, font=("Arial", 12))
    habit_entry.pack(pady=5)

    # Habit type selection
    habit_type_var = tk.StringVar(value="good")  # Default to "good"
    type_frame = tk.Frame(add_window)
    type_frame.pack(pady=10)

    type_label = tk.Label(type_frame, text="Select Habit Type:", font=("Arial", 12))
    type_label.pack(side=tk.LEFT)

    # Question mark label with tooltip for habit type
    question_label = tk.Label(type_frame, text=" (?)", font=("Arial", 12), fg="blue", cursor="question_arrow")
    question_label.pack(side=tk.LEFT)
    tooltip_text = ("Good habits help build positive routines and contribute to the tree's progress, "
                    "while bad habits might hinder your progress.")
    CreateToolTip(question_label, tooltip_text)

    # Radiobuttons for selecting the habit type
    radio_frame = tk.Frame(add_window)
    radio_frame.pack(pady=5)
    good_radio = tk.Radiobutton(radio_frame, text="Good", variable=habit_type_var, value="good", font=("Arial", 12))
    good_radio.pack(side=tk.LEFT, padx=10)
    bad_radio = tk.Radiobutton(radio_frame, text="Bad", variable=habit_type_var, value="bad", font=("Arial", 12))
    bad_radio.pack(side=tk.LEFT, padx=10)

    # Priority slider with tooltip
    priority_frame = tk.Frame(add_window)
    priority_frame.pack(pady=10)
    
    priority_label = tk.Label(priority_frame, text="Priority:", font=("Arial", 12))
    priority_label.pack(side=tk.LEFT)
    
    # Question mark label with tooltip for priority
    priority_question_label = tk.Label(priority_frame, text=" (?)", font=("Arial", 12), fg="blue", cursor="question_arrow")
    priority_question_label.pack(side=tk.LEFT)
    priority_tooltip_text = ("Priority affects how much the habit contributes to the water reward. "
                             "0 is highest priority while 5 is lowest.")
    CreateToolTip(priority_question_label, priority_tooltip_text)
    
    priority_slider = tk.Scale(add_window, from_=0, to=5, orient=tk.HORIZONTAL, font=("Arial", 12))
    priority_slider.set(0)  # Default priority
    priority_slider.pack(pady=5)

    # --- Days of the week selection ---
    days_frame = tk.Frame(add_window)
    days_frame.pack(pady=10)

    days_label = tk.Label(days_frame, text="Select Days:", font=("Arial", 12))
    days_label.grid(row=0, column=0, columnspan=7, pady=(0, 5))

    # Create checkbuttons for each day
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    day_vars = {}
    for idx, day in enumerate(days):
        var = tk.BooleanVar()
        chk = tk.Checkbutton(days_frame, text=day, variable=var, font=("Arial", 10))
        chk.grid(row=1, column=idx, padx=3)
        day_vars[day] = var

    # Functions to select and deselect all days
    def select_all_days():
        for var in day_vars.values():
            var.set(True)

    def deselect_all_days():
        for var in day_vars.values():
            var.set(False)

    # Buttons for selecting/deselecting all days
    select_all_button = tk.Button(days_frame, text="Select All", command=select_all_days, font=("Arial", 10))
    select_all_button.grid(row=2, column=1, columnspan=2, pady=5)
    
    deselect_all_button = tk.Button(days_frame, text="Deselect All", command=deselect_all_days, font=("Arial", 10))
    deselect_all_button.grid(row=2, column=4, columnspan=2, pady=5)

    # Button to add habit
    add_btn = tk.Button(
        add_window,
        text="Add Habit",
        font=("Arial", 12, "bold"),
        bg="#4CAF50",
        fg="white",
        padx=10,
        pady=5,
        command=lambda: add_habit(habit_entry, habit_type_var, priority_slider, day_vars, add_window, db_path, refresh_callback)
    )
    add_btn.pack(pady=15)
