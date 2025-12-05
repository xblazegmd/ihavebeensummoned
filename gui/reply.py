import tkinter as tk
from tkinter import ttk, messagebox

from core.comments import uploadComment
from core.errors import *

class ReplyBox(tk.Toplevel):
    def __init__(self, master, user: str, levelID: str, disabled: bool=False) -> None:
        super().__init__(master)
        self.user = user
        self.levelID = levelID
        self.disabled = disabled
        self.chars = 0

        self.title(f"Reply to @{self.user}")
        self.geometry("400x170")
        self.resizable(False, False)

        # Label
        label = ttk.Label(self, text=f"Reply to @{self.user} (ID: {self.levelID})")
        label.pack(pady=10)

        # The input's frame
        frame = ttk.Frame(self)
        frame.pack(pady=(10, 5))

        # The input B's StringVar
        self.inputBVar = tk.StringVar()
        self.inputBVar.trace_add("write", self.onInputBChange)
        
        # The inputs
        self.inputA = ttk.Entry(frame, width=9, validate="key", validatecommand=(self.master.register(self.validateInputA), "%P"))
        self.inputA.insert(0, f"@{self.user}")
        self.inputA.bind("<KeyRelease>", self.characterCountUpdate)
        self.inputA.pack(side="left", padx=(0, 5))

        self.inputB = ttk.Entry(frame, width=30, textvariable=self.inputBVar)
        self.inputB.pack(side="right")

        # The character label
        self.chatLabelVar = tk.StringVar()

        self.charLabel = ttk.Label(self, text="00/100")
        self.charLabel.pack(padx=(0, 330))

        # Reply button
        self.replyBt = ttk.Button(self, text="Reply", command=self.uploadComment, state=tk.DISABLED)
        self.replyBt.pack(pady=10)

        self.characterCountUpdate()
    
    def uploadComment(self) -> None:
        if self.disabled:
            return
        
        user = self.inputA.get()
        contents = self.inputBVar.get()
        comment = f"{user} {contents}"

        try:
            uploadComment(self.levelID, comment)
        except CooldownError as c:
            messagebox.showerror("Too fast", f"You'll be able to comment again in {c.remaining} seconds")
        except IHBSError:
            messagebox.showerror("Error", "Failed to upload comment")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        else:
            messagebox.showinfo("Success!", "Uploaded comment successfully")
            self.destroy()

    def characterCountUpdate(self, *_) -> bool:
        chars = len(self.inputA.get()) + len(self.inputBVar.get()) + 1
        remaining = 100 - chars

        self.charLabel.config(text=f"{remaining}/100")

        if remaining < 0:
            self.replyBt.config(state=tk.DISABLED)
            return False
        else:
            self.replyBt.config(state=tk.ACTIVE)
            return True

    @staticmethod
    def validateInputA(val: str) -> bool:
        if not val.startswith("@"):
            return False
        return True

    def onInputBChange(self, *_) -> None:
        contents = self.inputBVar.get()

        charCountStatus = self.characterCountUpdate()
        if not charCountStatus:
            return # AKA: bro it won't work already, don't check if the content's valid or not

        if contents == "":
            self.replyBt.config(state=tk.DISABLED)
        else:
            self.replyBt.config(state=tk.ACTIVE)
