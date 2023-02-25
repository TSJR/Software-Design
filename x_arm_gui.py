import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import font
from PIL import ImageTk, Image

# See b_and_w.py 
from b_and_w import *

from tkinter.ttk import *

# Name of selected image, used as global variable in a few functions
filename = ""

# Original, unedited image to keep returning back to 
original_img = None

# Current image label for the screen
pic = None

# PIL image that is used for the the pic label
pil_img = None

# Setting up tkinter window
window = tk.Tk()
window.title("xArm Drawing")
window.geometry("300x300")
window.configure(bg="#d1d1d1")

frame = tk.Frame(master=window, bg="#d1d1d1")
frame.pack(side=tk.BOTTOM, pady=50)

# Removing image from screen
def delete_img():
    if pic:
        pic.image = None
        pic.destroy()
        
# Not used here 
def get_brightness(rgb):
    rgb = [(val / 255) for val in rgb]
    brightness = 0
    brightness += rgb[0] * 0.21
    brightness += rgb[1] * 0.72
    brightness += rgb[2] * 0.07
    brightness *= 100
    return int(brightness)
    
# Threshold is value for a pixel to be considered black or white (see b_and_w.py for more)
# Updates the image with a new black and white one based on the new threshold (from slider)
def update_img(threshold):
    global pil_img, pic
    # Display width on screen
    abs_width = 500
    
    # Destroying old label if there is one
    if pic:
        pic.destroy()
       
    # Getting a new black and white image and resizing
    pil_img = get_black_and_white(original_img, round(float(threshold)))
    width, height = pil_img.size
    aspect_ratio = width / height
    pil_img = pil_img.resize((abs_width, int(abs_width / aspect_ratio)))
    
    # Setting pic label
    img = ImageTk.PhotoImage(pil_img)
    pic = tk.Label(window, image=img)
    pic.image = img
    pic.pack(expand=True)
    
# Image dialog to get file from user
def get_img():
    global pic, pil_img, original_img
    filename = askopenfilename()
    while "/" in filename:
        filename = filename[filename.index("/") + 1:]
    pil_img = Image.open(filename)
    original_img = pil_img
    img = ImageTk.PhotoImage(pil_img)

    # Default threshold is 50
    update_img(50)

# Setting up buttons and slider
delete = tk.Button(
    master=frame,
    text="Delete image",
    width=25,
    height=2,
    bg="white",
    fg="black",
    command=lambda:delete_img()
)
file_upload = tk.Button(
    master=frame,
    text="Upload image",
    width=25,
    height=2,
    bg="white",
    fg="black",
    command=lambda:get_img()
    
)
slider = Scale(frame, from_=0, to=100, orient=HORIZONTAL, command=update_img)

# Styling
delete["font"] = font.Font(family='Helvetica', size=24)
file_upload["font"] = font.Font(family='Helvetica', size=24)

# Placement on window
delete.grid(row=0, column=0, padx=5, pady=5)
file_upload.grid(row=0, column=2, padx=5, pady=5)
slider.grid(row = 0, column = 1, pady = 5)

# Main loop
window.mainloop()
