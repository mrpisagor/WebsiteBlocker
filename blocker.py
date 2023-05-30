import platform
import sys
from tkinter import ttk
import tkinter as tk
from dialog import get_input
from tkinter.messagebox import showwarning
from tkinter.messagebox import askyesno


class Blocker(tk.Tk):
    def __init__(self):
        super().__init__()
        self.cur_row = ""
        self.title("Website Blocker")

        self.geometry("800x375+400+200")
        self.resizable(False, False)

        self.host_file = self.get_host_file()

        self.img_checked = tk.PhotoImage(file="images/checked.png")
        self.img_unchecked = tk.PhotoImage(file="images/unchecked.png")

        self.list = ttk.Treeview(self, columns=("domain",))
        style = ttk.Style(self.list)
        style.configure("Treeview", rowheight=30)
        self.list.pack(fill=tk.X)
        self.list.heading("#0", text="")
        self.list.heading("domain", text="Domain")

        self.list.column("domain", anchor=tk.CENTER)

        self.update_list()
        self.menu = tk.Menu(self, tearoff=0)

        self.menu.add_command(label="remove", command=self.remove_website)

        self.list.tag_configure("checked", image=self.img_checked)
        self.list.tag_configure("unchecked", image=self.img_unchecked)
        self.list.bind("<Button-1>", self.toggleCheck)
        self.list.bind("<Button-3>", self.right_click)

        self.add_button = ttk.Button(self, text="Add", command=self.add_website)
        self.add_button.pack(pady=(10, 0))

    def start(self):
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.iconbitmap("images/block.ico")
        self.mainloop()

    def on_closing(self):
        if askyesno("Quitting", "All domains will be unblocked"):
            self.unblock_website(self.blacklist)
            self.destroy()

    @property
    def blacklist(self):
        with open("blacklist.txt", "r") as f:
            blacklist = f.read().splitlines()
            return blacklist

    def right_click(self, event):
        self.cur_row = self.list.identify_row(event.y)
        if self.cur_row:
            self.menu.tk_popup(event.x_root, event.y_root)

    def add_website(self):
        result = get_input()
        if result is not None:
            for rowid in self.list.get_children():
                domain = self.list.item(rowid, "values")[0]
                if domain == result:
                    return

            with open("blacklist.txt", "r+") as f:
                content = f.read()
                if content:
                    ends_newline = content[-1] == "\n"
                else:
                    ends_newline = True

                if ends_newline:
                    f.write(result + "\n")
                else:
                    f.write("\n" + result + "\n")

                self.block_website(result)
            self.update_list()

    def block_website(self, website):
        with open(self.host_file, "r+") as f:
            content = f.read()
            if website in content:
                return
            else:
                f.write(f"127.0.0.1 {website}\n")

    def unblock_website(self, domain):
        with open(self.host_file, "r") as reader:
            lines = reader.readlines()
            with open(self.host_file, "w") as writer:
                for line in lines:
                    if isinstance(domain, list):
                        if all(website not in line for website in domain):
                            writer.write(line)
                    else:
                        if domain not in line:
                            writer.write(line)

    def remove_website(self):
        row = self.list.item(self.cur_row)
        checked = True if "checked" == row["tags"][0] else False
        if not checked:
            domain = row["values"][0]
            content = self.blacklist
            with open("blacklist.txt", "w") as f:
                for line in content:
                    if domain not in line:
                        f.write(line + "\n")
            self.update_list()
        else:
            showwarning("Warning", "Please unblock before remove from list")

    def toggleCheck(self, event):
        rowid = self.list.identify_row(event.y)
        if rowid:
            domain = self.list.item(rowid, "values")[0]
            tag = self.list.item(rowid, "tags")[0]
            checked = True if tag == "checked" else False

            self.list.item(rowid, tags="unchecked" if checked else "checked")

            if checked:
                self.list.item(rowid, tags="unchecked")
                self.unblock_website(domain)

            else:
                self.list.item(rowid, tags="checked")
                self.block_website(domain)

    def update_list(self):
        self.list.delete(*self.list.get_children())
        for domain in self.blacklist:
            with open(self.host_file, "r") as f:
                content = f.read()
                if domain in content:
                    checked = True
                else:
                    checked = False
                self.list.insert("", tk.END, values=(domain,), tags="checked" if checked else "unchecked")

    @staticmethod
    def get_host_file():
        system_os = platform.system()
        if system_os == "Windows":
            host_file = "C:\\Windows\\System32\\drivers\\etc\\hosts"
        elif system_os == "Linux":
            host_file = "/etc/hosts"
        elif system_os == "Darwin":
            host_file = "/private/etc/hosts"
        else:
            sys.exit(0)
        return host_file
