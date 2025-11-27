import tkinter as tk
from tkinter import ttk, messagebox

from ..reply import ReplyBox
from ..tagPrompt import TagPrompt
from ..user.login import LoginWindow
from ..user.password import PasswordPrompt

class Prompts(tk.Toplevel):
    def __init__(self, master) -> None:
        super().__init__(master)

        self.title("Open Prompt")
        self.geometry("300x600")
        self.resizable(False, False)

        self.disabled = tk.BooleanVar()
        self.disabled.set(value=True)

        disabledCheck = ttk.Checkbutton(self, text="Disabled mode", variable=self.disabled)
        disabledCheck.pack(pady=20)

        replyBt = ttk.Button(self, text="ReplyBox", command=self.openReplyBox)
        replyBt.pack(pady=(0, 5))

        tagBt = ttk.Button(self, text="TagPrompt", command=self.openTagPrompt)
        tagBt.pack(pady=(0, 5))

        loginBt = ttk.Button(self, text="LoginWindow", command=self.openLoginWindow)
        loginBt.pack(pady=(0, 5))

        passwordBt = ttk.Button(self, text="PasswordPrompt", command=self.openPasswordPrompt)
        passwordBt.pack(pady=(0, 5))
    
    def warnIfNotDisabled(self) -> bool:
        if not self.disabled.get():
            return messagebox.askyesno(
                title="Warning",
                message="Running enabled prompts with this method can cause unexpected behavior. Are you sure you want to continue?"
            )
        return True

    def openReplyBox(self) -> None:
        if not self.warnIfNotDisabled():
            return
        ReplyBox(self.master, "testuser", "0", disabled=self.disabled.get())

    def openTagPrompt(self) -> None:
        if not self.warnIfNotDisabled():
            return
        TagPrompt(self.master, disabled=self.disabled.get())

    def openLoginWindow(self) -> None:
        if not self.warnIfNotDisabled():
            return
        LoginWindow(self.master, disabled=self.disabled.get())

    def openPasswordPrompt(self) -> None:
        if not self.warnIfNotDisabled():
            return
        PasswordPrompt(self.master, disabled=self.disabled.get())
