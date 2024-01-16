from tkinter import *
import subprocess
from PIL import Image, ImageTk

# Create the main Tkinter window
root = Tk()
root.title("Popflix - Profile Window")
root.geometry("989x605")
root.configure(bg='black')
root.resizable(0, 0)

# Function to open a separate file (search window)
def open_new_window():
    root.destroy()
    subprocess.run(["python", "search_window.py"])

# Function to open a separate file (view window)
def open_new_window_2():
    root.destroy()
    subprocess.run(["python", "view_window.py"])

# Frame 3 - Profile
profile = Frame(root, width=989, height=605, bd=0, highlightthickness=0)

# Load and display the profile background image
image = Image.open("Asset/profile.png")
resize_image = image.resize((989, 605))
profile_image = ImageTk.PhotoImage(resize_image)
bg_image_profile = Label(profile, image=profile_image)
bg_image_profile.place(x=-2, y=-2)

# Load and display profile buttons with different images and commands
profile_1 = ImageTk.PhotoImage(Image.open("Asset/profile_1.png"))
profile_1_button = Button(profile, image=profile_1, border=0, 
                          activebackground="#AA0001", foreground="black", 
                          bg="black", command=open_new_window)
profile_1_button.place(relx=.3, rely=.37)

profile_2 = ImageTk.PhotoImage(Image.open("Asset/profile_2.png"))
profile_2_button = Button(profile, image=profile_2, border=0, 
                          activebackground="#5825FE", foreground="black", 
                          bg="black", command=open_new_window_2)
profile_2_button.place(relx=.52, rely=.37)

profile.place(x=0, y=0)

# Run the Tkinter main loop
root.mainloop()
