
# Function to destroy the widgets
from PIL import Image, ImageTk
import tkinter as tk

def clear_widgets(root):
    for i in root.winfo_children():
        i.destroy()


def set_background(root, image_file_path, background_colour):
    img = Image.open(image_file_path)
    photo = ImageTk.PhotoImage(img)
    label = tk.Label(root, image=photo, bg=background_colour)
    label.image = photo
    label.place(x=0, y=0, relwidth=1, relheight=1)
