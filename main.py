import tkinter as tk
from tkinter import filedialog, Menu
from PIL import Image, ImageTk
import cv2
import numpy as np

RECENT_FILE_PATH = 'recent_files.txt'
MAX_RECENT_FILES = 5

def open_image(filepath=None):
    if filepath is None:
        filepath = filedialog.askopenfilename()
    if filepath:
        image = cv2.imread(filepath)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image)
        
        # Calculate the new size of the image
        ratio = min((root.winfo_screenwidth() * 0.8) / image_pil.width, (root.winfo_screenheight() * 0.7) / image_pil.height)
        new_size = (int(image_pil.width * ratio), int(image_pil.height * ratio))
        image_pil = image_pil.resize(new_size, Image.LANCZOS)
        
        image_tk = ImageTk.PhotoImage(image_pil)
        # Adjust the coordinates to place the image in the center of the green section
        x = root.winfo_screenwidth() * 0.2 + (root.winfo_screenwidth() * 0.8 - new_size[0]) / 2
        y = (root.winfo_screenheight() * 0.7 - new_size[1]) / 2
        canvas.create_image(x, y, image=image_tk, anchor='nw')
        canvas.image_tk = image_tk
        canvas.image_pil = image_pil 
        save_in_recent(filepath)

def save_in_recent(filepath):
    recent_files = open_recent()
    if filepath not in recent_files:
        with open(RECENT_FILE_PATH, 'a') as f:
            f.write(filepath + '\n')

def open_recent():
    try:
        with open(RECENT_FILE_PATH, 'r') as f:
            lines = f.readlines()
            recent_files = [line.strip() for line in lines[-MAX_RECENT_FILES:]]
            return recent_files
    except FileNotFoundError:
        return []
    
root = tk.Tk()
root.state('zoomed')

toolbar = Menu(root)
root.config(menu=toolbar)

file_menu = Menu(toolbar, tearoff=0)
toolbar.add_cascade(label="Arquivo", menu=file_menu)
file_menu.add_command(label="Abrir imagem", command=open_image)

recent_menu = Menu(file_menu, tearoff=0)
file_menu.add_cascade(label="Abrir recente", menu=recent_menu)
for file in open_recent():
    recent_menu.add_command(label=file, command=lambda file=file: open_image(file))

operation_menu = Menu(toolbar, tearoff=0)
toolbar.add_cascade(label="Operações", menu=operation_menu)
operation_menu.add_command(label="Filtros")

canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
canvas.pack()

x1 = 0
y1 = 0
x2 = int(root.winfo_screenwidth() * 0.2)
y2 = root.winfo_screenheight()
canvas.create_rectangle(x1, y1, x2, y2)#, fill='red')

x1 = x2
x2 = root.winfo_screenwidth()
y2 = int(root.winfo_screenheight() * 0.7)
canvas.create_rectangle(x1, y1, x2, y2)#, fill='green')

y1 = y2
y2 = root.winfo_screenheight()
canvas.create_rectangle(x1, y1, x2, y2)#, fill='blue')

root.mainloop()