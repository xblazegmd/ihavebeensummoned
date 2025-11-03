import tkinter as tk
from tkinter import messagebox, ttk

from core.saveFile import loadData
from core.security import saveGJP, generateGJP
from core.user import logIn
from utils import changeFontSize

class PasswordPrompt(tk.Toplevel):
    def __init__(self, master) -> None:
        super().__init__(master)
        self.data = loadData()
        self.username = self.data.get("username")

        self.title(f"Welcome Back {self.username}")
        self.geometry("300x200")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.onClose)

        label = ttk.Label(self, text="Password:")
        label.pack(padx=(0, 124), pady=(30, 5))

        frame = ttk.Frame(self)
        frame.pack()
        
        self.password = ttk.Entry(frame, show="*", width=15)
        self.password.pack(side="left", fill="x")

        self.visBt = ttk.Button(frame, text="S", width=1, command=self.togglePasswordVis)
        self.visBt.pack(side="right")

        discText = """(For your privacy, your GD password wont be stored
                    anywhere on your device)"""
        disc = ttk.Label(self, text=discText)
        disc.configure(font=changeFontSize(disc, 8))
        disc.pack(pady=5)

        loginBt = ttk.Button(self, text="Login", command=self.logIn)
        loginBt.pack(pady=(2, 14))

    def togglePasswordVis(self) -> None:
        if self.password.cget("show") == "":
            self.password.config(show="*")
            self.visBt.config(text="S")
        else:
            self.password.config(show="")
            self.visBt.config(text="H")

    def logIn(self):
        password = self.password.get()

        if password == "":
            messagebox.showerror("Error", "Password was not specified")
            return

        if self.username is None:
            messagebox.showerror("Error", "Username was not found. Please reset your save file")
            return

        status = logIn(self.username, password)

        if status[0] == "-1":
            messagebox.showerror("Error", "An unexpected error happened")
        elif status[0] == "-2":
            messagebox.showerror("Error", "The specified user does not exist")
        elif status[0] == "-3":
            messagebox.showerror("Error", "Password is possibly incorrect. If this issue persists (even when the password is correct) report this issue to the GitHub")
        else:
            saveGJP(generateGJP(password))
            del password

            self.destroy()

    def onClose(self) -> None:
        self.master.destroy()
