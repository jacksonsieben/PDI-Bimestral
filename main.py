import copy
import tkinter as tk
from tkinter import filedialog, Menu, messagebox, ttk, simpledialog
from PIL import Image, ImageTk
import cv2
from models.operation import operation_list
from utils.operation_type import OperationType
from models.custom_dialog import CustomDialog

RECENT_FILE_PATH = 'recent_files.txt'
MAX_RECENT_FILES = 5

has_image : bool = False
original_image = None

def insert_image(image):
    if image is not None:
        if len(image.shape) == 2:
            image_pil = Image.fromarray(image, 'L')
        elif len(image.shape) == 3:
            image_pil = Image.fromarray(image, 'RGB')
        else:
            messagebox.showerror("Error", f"Ocorreu um erro ao inserir a imagem")
            return        
        ratio = min((image_frame.winfo_width()) / image_pil.width, image_frame.winfo_height() / image_pil.height)
        new_size = (int(image_pil.width * ratio), int(image_pil.height * ratio))
        image_pil = image_pil.resize(new_size, Image.LANCZOS)
        
        image_tk = ImageTk.PhotoImage(image_pil)
        x = (image_frame.winfo_width() - new_size[0]) / 2
        y = (image_frame.winfo_height() - new_size[1]) / 2
        canvas.create_image(x, y, image=image_tk, anchor='nw')
        canvas.image_tk = image_tk
        canvas.image_pil = image_pil

def open_image(filepath=None):
    global has_image, original_image, file_menu
    if filepath is None:
        filepath = filedialog.askopenfilename()
    if filepath:
        image = cv2.imread(filepath)
        if image is None:
            messagebox.showerror("Error", f"Failed to load image at {filepath}")
            return
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        original_image = image
        insert_image(image)
        has_image = True
        save_in_recent(filepath)
        file_menu.entryconfig("Salvar imagem", state="normal")

def save_in_recent(filepath):
    recent_files = open_recent()
    if filepath not in recent_files:
        with open(RECENT_FILE_PATH, 'a') as f:
            f.write(filepath + '\n')

def save_image():
    global has_image
    if has_image:
        filepath = filedialog.askopenfilename()
        if filepath:
            cv2.imwrite(filepath, canvas.image_pil)

def open_recent():
    try:
        with open(RECENT_FILE_PATH, 'r') as f:
            lines = f.readlines()
            recent_files = [line.strip() for line in lines[-MAX_RECENT_FILES:]]
            return recent_files
    except FileNotFoundError:
        return []
    
def create_menu(root):
    global operation_menu, file_menu
    toolbar = Menu(root)
    root.config(menu=toolbar)

    file_menu = Menu(toolbar, tearoff=0)
    toolbar.add_cascade(label="Arquivo", menu=file_menu)
    file_menu.add_command(label="Abrir imagem", command=open_image)

    recent_menu = Menu(file_menu, tearoff=0)
    file_menu.add_cascade(label="Abrir recente", menu=recent_menu)
    for file in open_recent():
        recent_menu.add_command(label=file, command=lambda file=file: open_image(file))

    file_menu.add_command(label="Salvar imagem", command=save_image, state="disabled")

    operation_menu = Menu(toolbar, tearoff=0)
    toolbar.add_cascade(label="Operações", menu=operation_menu)

    for operation_type, operations in operation_list.items():
        sub_menu = Menu(operation_menu, tearoff=0)
        operation_menu.add_cascade(label=operation_type.value, menu=sub_menu)
        for operation in operations:
            sub_menu.add_command(label=operation.display_name, command=lambda operation=operation: add_operation_to_listbox(operation))
    
    update_menu()

def update_menu():
    global operation_menu
    state_color="normal"
    state_binarization = "normal"
    state_morph = "disabled"
    submenu_state_filter = "normal"
    submenu_state_bin = "disabled"

    try:
        operations_added = {operation_type: listbox.get(0, tk.END) for operation_type, listbox in operation_listboxes.items()}
        if len(operations_added[OperationType.CONVERTION_COLOR]) > 0:
            state_color="disabled"
            if operations_added[OperationType.CONVERTION_COLOR][0] == "RGB para Cinza":
                submenu_state_filter = "disabled"
                submenu_state_bin = "normal"
        if len(operations_added[OperationType.BINARIZATION]) > 0:
            state_binarization="disabled"
            state_morph = "normal"
    except Exception as e:
        pass
    
    submenu_name = operation_menu.entrycget(OperationType.FILTER.value, 'menu')
    submenu = operation_menu.nametowidget(submenu_name)

    for i in range(submenu.index('end')+1):
        if i in (0, 2):
            submenu.entryconfig(i, state=submenu_state_filter)

    submenu_name = operation_menu.entrycget(OperationType.BINARIZATION.value, 'menu')
    submenu = operation_menu.nametowidget(submenu_name)

    for i in range(submenu.index('end')+1):
        if i == 1:
            submenu.entryconfig(i, state=submenu_state_bin)

    operation_menu.entryconfig(OperationType.CONVERTION_COLOR.value, state=state_color)
    operation_menu.entryconfig(OperationType.BINARIZATION.value, state=state_binarization)
    operation_menu.entryconfig(OperationType.MATH_MORPH.value, state=state_morph)
    

def add_operation_to_listbox(operation, is_edit=False):
    global original_image
    if has_image:
        if operation.input_parameters:
            for i, input_name in enumerate(operation.input_parameters):
                if input_name is not None:
                    correct_input = False
                    existing_value=None
                    if is_edit and hasattr(operation, 'input_values') and operation.parameters[i] is not None:
                        existing_value = operation.input_values[input_name]
                    while not correct_input:
                        error = False
                        dialog = CustomDialog(root, title="Input", prompt=f"Digite o valor de {input_name}", initial_value=existing_value)
                        
                        if dialog.input is None or dialog.input == '':
                            if not dialog.ok_pressed:
                                return
                            messagebox.showerror("Error", f"Campo obrigatório {input_name} não preenchido")
                            error = True
                        
                        try:
                            if not dialog.input.isdigit() and int(dialog.input) > 0 and int(dialog.input) < 255 and not error:
                                messagebox.showerror("Error", f"O valor de {input_name} deve ser um número inteiro entre 0 e 255")
                                error = True
                        except ValueError:
                            messagebox.showerror("Error", f"O valor de {input_name} deve ser um número")
                            error = True
                        
                        if input_name == "blockSize":
                            if int(dialog.input) % 2 == 0 and not error:
                                messagebox.showerror("Error", f"O valor de {input_name} deve ser um número ímpar")
                                error = True

                        if not hasattr(operation, 'input_values'):
                            operation.input_values = {}
                        
                        if not error:
                            correct_input = True

                    operation.input_values[input_name] = int(dialog.input)
                    param = int(dialog.input) if input_name != "Kernel Size" else (int(dialog.input), int(dialog.input))
                    operation.parameters[operation.input_parameters.index(input_name)] = param
        
        operation.image = original_image
        
        if not is_edit:
            operation_listboxes[operation.type].insert(tk.END, operation.get_display_name())
            update_menu()
        else:
            update_menu()
            return operation
    else:
        messagebox.showerror("Error", f"Abra uma imagem antes de adicionar operações")
        return

def edit_operation(listbox):
    try:
        selected_index = listbox.curselection()

        if selected_index:
            operation_type = [key for key, value in operation_listboxes.items() if value == listbox][0]
            operation = operation_list[operation_type][selected_index[0]]

            dialog = CustomDialog(root, title="Selecione uma operação", operations=operation_list[operation_type])

            if dialog.input is None:
                if not dialog.ok_pressed:
                    return
                messagebox.showerror("Error", "Nenhuma operação selecionada")
                return

            operation_name = dialog.input
            operation = find_operation_by_name(operation_list[operation_type], operation_name)

            edited_operation = add_operation_to_listbox(operation, True)
            if edited_operation is not None:
                listbox.delete(selected_index)
                listbox.insert(selected_index, edited_operation.get_display_name())

    except Exception as e:
        messagebox.showerror("Error", str(e))
    
def find_operation_by_name(operations, operation_name):
    return next((operation for operation in operations if operation.display_name == operation_name or operation.get_display_name() == operation_name), None)

def execute_operations():
    image = original_image.copy()
    for operation_type, listbox in operation_listboxes.items():
        for index in range(listbox.size()):
            operation_name = listbox.get(index)
            operation = find_operation_by_name(operation_list[operation_type], operation_name)
            if operation is not None:
                try:
                    image = operation.apply_method(image)
                except Exception as e:
                    messagebox.showerror("Error", str(e))
    insert_image(image)

def show_context_menu(event):
    context_menu = tk.Menu(root, tearoff=0)
    context_menu.add_command(label="Editar", command=lambda: edit_operation(event.widget))
    context_menu.add_command(label="Remover", command=lambda: remove_operation(event.widget))
    context_menu.add_command(label="Duplicar", command=lambda: duplicate_operation(event.widget))

    context_menu.tk_popup(event.x_root, event.y_root)

def remove_operation(listbox):
    selected_operation = listbox.curselection()

    if selected_operation:
        listbox.delete(selected_operation)

    update_menu()

def duplicate_operation(listbox):
    selected_index = listbox.curselection()

    if selected_index:
        operation_type = [key for key, value in operation_listboxes.items() if value == listbox][0]
        operation = find_operation_by_name(operation_list[operation_type], listbox.get(selected_index[0]))

        duplicated_operation = copy.deepcopy(operation)

        listbox.insert(selected_index[0] + 1, duplicated_operation.get_display_name())

    update_menu()

def on_listbox_select(event):
    listbox = event.widget
    selected_operation = listbox.curselection()

    if selected_operation:
        operation_type = [key for key, value in operation_listboxes.items() if value == listbox][0]
        selected_operation = operation_list[operation_type][selected_operation[0]]

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
