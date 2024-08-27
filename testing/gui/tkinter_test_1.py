import tkinter as tk
from tkinter import messagebox

def on_submit_click():
    user_input = entry.get()
    messagebox.showinfo("Information",f"You entered: {user_input}")

def on_exit_click():
    root.destroy()

# Create the main window
root = tk.Tk()
root.geometry("{}x{}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.title("Raspberry Pi GUI")

# Set the window size
# screen_width = 1024
# screen_height = 600
# pos_right = int(root.winfo_screenwidth()/2 - screen_width/2) - 100
# pos_down = int(root.winfo_screenheight()/2 - screen_height/2)
# root.geometry(f"{screen_width}x{screen_height}+{pos_right}+{pos_down}")


# Create a label
label = tk.Label(root, text="Enter something:")
label.pack(pady=10)

# Create an entry field
entry = tk.Entry(root)
entry.pack(pady=5)

# Create a submit button
submit_button = tk.Button(root, text="Submit", font=("Helvetica", 24), command=on_submit_click)
submit_button.pack(pady=10)

# Create an exit button
exit_button = tk.Button(root, text="Exit", font=("Helvetica",24), command=on_exit_click)
exit_button.pack(pady=20)

# Start the Tkinter event loop
root.mainloop()

