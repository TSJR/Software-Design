import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import font
from PIL import ImageTk, Image
import pygame
from BlackAndWhite import *
from tkinter.ttk import *

filename = ""

original_img = None
pic = None
pil_img = None

window = tk.Tk()
window.title("xArm Drawing")
window.geometry("300x300")
window.configure(bg="#d1d1d1")

frame = tk.Frame(master=window, bg="#d1d1d1")
frame.pack(side=tk.BOTTOM, pady=50)

def delete_img():
    if pic:
        pic.image = None
        pic.destroy()

def get_brightness(rgb):
    rgb = [(val / 255) for val in rgb]
    brightness = 0
    brightness += rgb[0] * 0.21
    brightness += rgb[1] * 0.72
    brightness += rgb[2] * 0.07
    brightness *= 100
    return int(brightness)
    
def update_img(threshold):
    global pil_img, pic
    abs_width = 500
    if pic:
        pic.destroy()
    pil_img = get_black_and_white(original_img, round(float(threshold)))
    width, height = pil_img.size
    aspect_ratio = width / height
    pil_img = pil_img.resize((abs_width, int(abs_width / aspect_ratio)))
    
    img = ImageTk.PhotoImage(pil_img)
    pic = tk.Label(window, image=img)
    pic.image = img
    pic.pack(expand=True)
    

def get_img():
    global pic, pil_img, original_img
    filename = askopenfilename()
    while "/" in filename:
        filename = filename[filename.index("/") + 1:]
    pil_img = Image.open(filename)
    original_img = pil_img
    img = ImageTk.PhotoImage(pil_img)

    update_img(50)
    
  


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

delete["font"] = font.Font(family='Helvetica', size=24)
file_upload["font"] = font.Font(family='Helvetica', size=24)



delete.grid(row=0, column=0, padx=5, pady=5)
file_upload.grid(row=0, column=2, padx=5, pady=5)
slider.grid(row = 0, column = 1, pady = 5)


  
print(str(get_brightness((100, 10, 50))) + "%")

new_threshold = slider.get

window.mainloop()
