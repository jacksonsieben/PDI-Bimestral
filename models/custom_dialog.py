from tkinter import simpledialog
import tkinter as tk

class CustomDialog(simpledialog.Dialog):
    def __init__(self, parent, title=None, prompt=None, initial_value=None, **kwargs):
        self.prompt = prompt
        self.input = initial_value
        super().__init__(parent, title=title, **kwargs)

    def body(self, master):
        self.label = tk.Label(master, text=self.prompt)
        self.label.pack()
        self.entry = tk.Entry(master)
        if self.input:
            self.entry.insert(0, self.input)
        self.entry.pack()
        return self.entry

    def apply(self):
        self.input = self.entry.get()