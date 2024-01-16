from tkinter import *
import subprocess
from PIL import Image, ImageTk

# Create the main Tkinter window
root = Tk()
root.title("Popflix - Opening Window")
root.geometry("989x605")
root.configure(bg='black')
root.resizable(0, 0)

# Function to show a specific frame
def show_frame(frame):
    frame.tkraise()

# Function to open a separate file (search window)
def open_new_window():
    root.destroy()
    subprocess.run(["python", "profile_window.py"])

# Frame 1 - Home
home = Frame(root, width=989, height=605, bd=0, highlightthickness=0)

# Load and display the home background image
image = Image.open("Asset/home.png")
resize_image = image.resize((989, 605))
home_image = ImageTk.PhotoImage(resize_image)
bg_image_home = Label(home, image=home_image)
bg_image_home.place(x=-2, y=-2)

# Button to navigate to the instructions frame
start_button = Button(home, text="Start", bg="red", fg="black", 
                      activebackground="red", font=('Roboto', 15, 'bold'), 
                      relief="flat", command=lambda: show_frame(instructions))
start_button.place(relx=.45, rely=.63, width=110, height=45)
home.place(x=0, y=0)

# Frame 2 - Instructions
instructions = Frame(root, width=989, height=605, bd=0, highlightthickness=0)

# Load and display the instructions background image
image = Image.open("Asset/instructions.png")
resize_image = image.resize((989, 605))
instructions_image = ImageTk.PhotoImage(resize_image)
bg_image_instructions = Label(instructions, image=instructions_image)
bg_image_instructions.place(x=-2, y=-2)

# Button to navigate to the profile frame
next_button = Button(instructions, text="Next", bg="red", fg="black", 
                     activebackground="red", font=('Roboto', 13, 'bold'), 
                     relief="flat", command=open_new_window)
next_button.place(relx=.45, rely=.77, width=100, height=45)
instructions.place(x=0, y=0)

# Initial frame to show is the home frame
show_frame(home)

# Run the Tkinter main loop
root.mainloop()
