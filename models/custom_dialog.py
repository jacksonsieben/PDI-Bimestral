from tkinter import simpledialog
import tkinter as tk

class CustomDialog(simpledialog.Dialog):
    def __init__(self, parent, title=None, prompt=None, initial_value=None, operations=None, **kwargs):
        self.prompt = prompt
        self.input = initial_value
        self.operations = operations
        self.ok_pressed = False  # Flag to check if the OK button was pressed
        super().__init__(parent, title=title, **kwargs)

    def body(self, master):
        self.label = tk.Label(master, text=self.prompt)
        self.label.pack()
        
        if self.operations:
            self.listbox = tk.Listbox(master, width=35)
            for operation in self.operations:
                self.listbox.insert(tk.END, operation.display_name)
            self.listbox.pack()
        else:
            self.entry = tk.Entry(master)
            if self.input:
                self.entry.insert(0, self.input)
            self.entry.pack()

        self.grab_set()

        return self.entry if not self.operations else self.listbox

    def buttonbox(self):
        box = tk.Frame(self)

        ok_button = tk.Button(box, text="OK", width=10, command=self.ok, default="active")
        ok_button.pack(side="left", padx=5, pady=5)

        cancel_button = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        cancel_button.pack(side="left", padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    def ok(self, event=None):
        self.ok_pressed = True  # Set the flag to True when the OK button is pressed
        super().ok(event)

    def apply(self):
        if self.ok_pressed:  # Only get the input if the OK button was pressed
            self.input = self.entry.get() if not self.operations else self.listbox.get(self.listbox.curselection())