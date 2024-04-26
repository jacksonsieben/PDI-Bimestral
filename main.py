import tkinter as tk
from tkinter import filedialog, Menu, messagebox, ttk, simpledialog
from PIL import Image, ImageTk
import cv2
import numpy as np
from models.operation import operation_list
from utils.operation_type import OperationType
from models.custom_dialog import CustomDialog

RECENT_FILE_PATH = 'recent_files.txt'
MAX_RECENT_FILES = 5

has_image : bool = False


def open_image(filepath=None):
    global has_image
    if filepath is None:
        filepath = filedialog.askopenfilename()
    if filepath:
        image = cv2.imread(filepath)
        if image is None:
            messagebox.showerror("Error", f"Failed to load image at {filepath}")
            return
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image)
        
        ratio = min((image_frame.winfo_width()) / image_pil.width, image_frame.winfo_height() / image_pil.height)
        new_size = (int(image_pil.width * ratio), int(image_pil.height * ratio))
        image_pil = image_pil.resize(new_size, Image.LANCZOS)
        
        image_tk = ImageTk.PhotoImage(image_pil)
        x = (image_frame.winfo_width() - new_size[0]) / 2
        y = (image_frame.winfo_height() - new_size[1]) / 2
        canvas.create_image(x, y, image=image_tk, anchor='nw')
        canvas.image_tk = image_tk
        canvas.image_pil = image_pil 
        has_image = True
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
    
def create_menu(root):
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

    for operation_type, operations in operation_list.items():
        sub_menu = Menu(operation_menu, tearoff=0)
        operation_menu.add_cascade(label=operation_type.value, menu=sub_menu)
        for operation in operations:
            sub_menu.add_command(label=operation.display_name, command=lambda operation=operation: add_operation_to_listbox(operation))

def add_operation_to_listbox(operation, is_edit=False):
    if has_image:
        if operation.input_parameters:
            for input_name in operation.input_parameters:
                correct_input = False
                existing_value=None
                if is_edit:
                    existing_value = operation.input_values[input_name]
                while not correct_input:
                    error = False
                    dialog = CustomDialog(root, title="Input", prompt=f"Digite o valor de {input_name}", initial_value=existing_value)
                    
                    if dialog.input is None or dialog.input == '':
                        messagebox.showerror("Error", f"Campo obrigatório {input_name} não preenchido")
                        error = True
                    
                    if not dialog.input.isdigit() and not error:
                        messagebox.showerror("Error", f"O valor de {input_name} deve ser um número inteiro")
                        error = True
                    
                    if not hasattr(operation, 'input_values'):
                        operation.input_values = {}

                    if not error:
                        correct_input = True

                operation.input_values[input_name] = int(dialog.input)
        if not is_edit:
            operation_listboxes[operation.type].insert(tk.END, operation.get_display_name())
        else:
            return operation
    else:
        messagebox.showerror("Error", f"Abra uma imagem antes de adicionar operações")
        return
    
def edit_operation(listbox):
    selected_index = listbox.curselection()

    if selected_index:
        operation_type = [key for key, value in operation_listboxes.items() if value == listbox][0]
        operation = operation_list[operation_type][selected_index[0]]

        edited_operation = add_operation_to_listbox(operation, True)

        operation_list[operation_type][selected_index[0]] = edited_operation

        listbox.delete(selected_index)
        listbox.insert(selected_index, edited_operation.get_display_name())
        

def execute_operations():
    for operation_type, listbox in operation_listboxes.items():
        for index in range(listbox.size()):
            operation = operation_list[operation_type][index]
            print(operation.get_display_name())

def show_context_menu(event):
    context_menu = tk.Menu(root, tearoff=0)
    context_menu.add_command(label="Editar", command=lambda: edit_operation(event.widget))
    context_menu.add_command(label="Remover", command=lambda: remove_operation(event.widget))

    context_menu.tk_popup(event.x_root, event.y_root)

def remove_operation(listbox):
    selected_operation = listbox.curselection()

    if selected_operation:
        listbox.delete(selected_operation)


def on_listbox_select(event):
    listbox = event.widget
    selected_operation = listbox.curselection()

    if selected_operation:
        operation_type = [key for key, value in operation_listboxes.items() if value == listbox][0]
        selected_operation = operation_list[operation_type][selected_operation[0]]
        print(selected_operation.display_name)

root = tk.Tk()
root.state('zoomed')

create_menu(root)

operation_frame = tk.Frame(root, bg='light gray')
operation_frame.place(relx=0, rely=0, relwidth=0.3, relheight=1.0)

separator = ttk.Separator(root, orient='vertical')
separator.place(relx=0.3, rely=0, relheight=1.0)

image_frame = tk.Frame(root, bg='white')
image_frame.place(relx=0.3, rely=0, relwidth=0.7, relheight=1.0)

canvas = tk.Canvas(image_frame, bg='white')
canvas.pack(fill='both', expand=True)

operation_listboxes = {operation_type: tk.Listbox(operation_frame,  justify='center') for operation_type in OperationType}
for operation_type in OperationType:
    operation_listboxes[operation_type].bind("<Button-1>", on_listbox_select)
    operation_listboxes[operation_type].bind("<Button-3>", show_context_menu)
    operation_listboxes[operation_type].pack(fill='both', expand=True)

execute_button = tk.Button(operation_frame, text="Aplicar operações", command=execute_operations)
execute_button.pack(pady=10, padx=10, fill='both', expand=True)

root.mainloop()
