from tkinter.messagebox import showwarning
import tkinter as tk
from tkinter import ttk


class InputDialog(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.geometry("250x90+625+355")
        self.resizable(False, False)
        self.result = None
        self.website_val = tk.StringVar(self)
        self.label = ttk.Label(self, text="Enter domain")
        self.label.pack(pady=(10, 0))
        self.website_entry = ttk.Entry(self, textvariable=self.website_val, width=30)
        self.website_entry.pack(pady=(0, 10))
        self.buttons_frame = ttk.Frame(self)

        self.ok_button = ttk.Button(self.buttons_frame, text="ok", command=self.ok_pressed)
        self.ok_button.grid(row=0, column=0,padx=(0,5))
        self.cancel_button = ttk.Button(self.buttons_frame, text="cancel", command=self.cancel_pressed)
        self.cancel_button.grid(row=0, column=1,padx=(5,0))

        self.buttons_frame.pack(anchor=tk.CENTER)

        self.iconbitmap("images/block.ico")

    def ok_pressed(self):
        if self.website_val.get():
            self.result = self.website_val.get()
            self.destroy()
        else:
            showwarning("Empty Field", "Field cannot be empty!")

    def cancel_pressed(self):
        self.destroy()


def get_input():
    dialog = InputDialog()
    dialog.wait_window()
    return dialog.result
