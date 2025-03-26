from tkinter import *
from sqlite import *

def donothing():
    # Placeholder function for menu commands
    pass

def create_top_menu(root):
    # Create the top-level menu and configure the window to use it
    menu = Menu(root)
    root.config(menu=menu)
    
    # File menu
    file_menu = Menu(menu, tearoff=0)
    file_menu.add_command(label="New", command=lambda:createDatabase(root))
    file_menu.add_command(label="Open", command=lambda:importDatabase(root))
    file_menu.add_command(label="Save", command=donothing)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)
    menu.add_cascade(label="File", menu=file_menu)
    
    # Help menu
    help_menu = Menu(menu, tearoff=0)
    help_menu.add_command(label="About", command=donothing)
    menu.add_cascade(label="Help", menu=help_menu)
