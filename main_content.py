from tkinter import *
from tkinter import ttk

def show_main_page(root):
    # Clear existing widgets from the root window
    for widget in root.winfo_children():
        widget.destroy()
    
    # Create and configure the main container frame
    main_frame = Frame(root)
    main_frame.pack(pady=20)
    
    # "My Tree" label
    lbl_title = Label(main_frame, text="My Tree", font=('Arial', 16, 'bold'))
    lbl_title.pack(pady=10)
    
    # Tree image (update the file extension if needed)
    try:
        tree_image = PhotoImage(file="Tree/tree_stage_6.png")
        lbl_image = Label(main_frame, image=tree_image)
        lbl_image.image = tree_image  # Keep reference
        lbl_image.pack(pady=10)
    except Exception as e:
        print(f"Error loading image: {e}")
    
    # Progress bar
    progress = ttk.Progressbar(
        main_frame, 
        orient=HORIZONTAL, 
        length=300, 
        mode='determinate'
    )
    progress.pack(pady=10)
    progress['value'] = 60  # Set your initial value here