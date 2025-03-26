from tkinter import *
from sqlite import *

def donothing():
    pass

def create_top_menu(root, content_frame):
    # Clear existing widgets from the content_frame only
    for widget in content_frame.winfo_children():
        widget.destroy()

    menu = Menu(root)
    root.config(menu=menu)
    
    file_menu = Menu(menu, tearoff=0)
    # Use the passed content_frame in your lambda functions
    file_menu.add_command(label="New", command=lambda: createDatabase(content_frame))
    file_menu.add_command(label="Open", command=lambda: importDatabase(content_frame))
    file_menu.add_command(label="Save", command=donothing)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)
    menu.add_cascade(label="File", menu=file_menu)
    
    help_menu = Menu(menu, tearoff=0)
    help_menu.add_command(label="About", command=donothing)
    menu.add_cascade(label="Help", menu=help_menu)
