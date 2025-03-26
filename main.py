from tkinter import *
from top_menu import create_top_menu
from file_manager import *

root = Tk()
root.title("Habit Tree")
root.geometry('400x600')

# Create the content frame before setting up the top menu
content_frame = Frame(root)
content_frame.pack(pady=50)

# Pass the content frame to the menu creation function
create_top_menu(root, content_frame)

root.mainloop()
