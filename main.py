from tkinter import *
from top_menu import create_top_menu
from file_manager import *

# Create the main window
root = Tk()
root.title("Habit Tree")

# Set up the top menu from our external module
create_top_menu(root)

# Create a canvas widget
canvas = Canvas(root, width=400, height=300, bg='white')
canvas.pack()

# Start the main event loop
root.mainloop()
