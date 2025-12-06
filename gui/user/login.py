import tkinter as tk
from tkinter import ttk, messagebox

from core.errors import *
from core.user import logIn
from core.saveFile import updateData
from core.security import saveGJP, generateGJP
from utils import changeFontSize, logger

class LoginWindow(tk.Toplevel):
    def __init__(self, master, disabled: bool=False) -> None:
        super().__init__(master)
        self.disabled = disabled

        self.title("Log In")
        self.geometry("400x250")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.onClose)

        # Username entry
        labelUser = ttk.Label(self, text="Username:")
        labelUser.pack(padx=(0, 122), pady=(10, 5))

        self.username = ttk.Entry(self)
        self.username.pack()

        # Password entry
        labelPass = ttk.Label(self, text="Password:")
        labelPass.pack(padx=(0, 124), pady=(10, 5))

        # Password entry frame
        frame = ttk.Frame(self)
        frame.pack()

        self.password = ttk.Entry(frame, show="*", width=15)
        self.password.pack(side="left", fill="x")
        self.visBt = ttk.Button(frame, text="S", width=1, command=self.togglePasswordVis)
        self.visBt.pack(side="right")

        # Disclaimer label
        labelDiscText = """(For your privacy, your GD password wont be stored
                    anywhere on your device)"""
        labelDisc = ttk.Label(self, text=labelDiscText)
        labelDisc.configure(font=changeFontSize(labelDisc, 8))
        labelDisc.pack(pady=5)

        loginBt = ttk.Button(self, text="Login", command=self.logIn)
        loginBt.pack(pady=14)
    
    def togglePasswordVis(self) -> None:
        if self.password.cget("show") == "":
            self.password.config(show="*")
            self.visBt.config(text="S")
        else:
            self.password.config(show="")
            self.visBt.config(text="H")
    
    def logIn(self) -> None:
        if self.disabled:
            return

        username = self.username.get()
        password = self.password.get()

        if username == "" or password == "":
            messagebox.showerror("Error", "Incomplete details")
            return

        try:
            status = logIn(username, password)
        except NotFoundError:
            messagebox.showerror("Error", "The specified user does not exist")
        except AuthError:
            messagebox.showerror("Error", "Password is possibly incorrect. If this issue persists (even when the password is correct) report this issue to the GitHub")
        except BoomlingsError as b:
            messagebox.showerror("Error", str(b))
        except Exception as e:
            logger.error(str(e))
            messagebox.showerror("Error", "An unexpected error occurred. Plese report this issue to the GitHub, alongside the program's logs")
        else:
            messagebox.showinfo("Logged in", f"You are now logged in as @{username}")

            try:
                updateData(username=username, accID=status[1])
            except SFWriteError as s:
                logger.error(str(s))
                messagebox.showerror("Error", "Could not save data to the program's save file")
                return

            saveGJP(generateGJP(password))
            del password

            self.destroy()
    
    def onClose(self) -> None:
        if self.disabled:
            self.destroy()
            return

        self.master.destroy()
