import tkinter as tk

from tkinter import ttk, messagebox
from utils import notify
from .reply import ReplyBox

class ListenerWindow(tk.Toplevel):
    def __init__(self, master, levelID: str) -> None:
        super().__init__(master)
        self.levelID = levelID
        
        self.title("Mentions")
        self.geometry("600x300")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.onClose)

        # The label up top
        label = ttk.Label(self, text=f"All mentions on {levelID}:")
        label.pack(pady=10)

        # The mention list (ttk.Treeview)
        self.mentions = ttk.Treeview(self, columns=("user", "comment"), show="headings", height=8)

        self.mentions.heading("user", text="User")
        self.mentions.heading("comment", text="Comment")

        self.mentions.column("user", width=200)
        self.mentions.column("comment", width=350)

        self.mentions.bind("<<TreeviewSelect>>", self.onItemSelected)
         
        self.mentions.pack(pady=10)

        # The reply button
        self.replyBt = ttk.Button(self, text="Reply", command=self.replyToMention, state=tk.DISABLED)
        self.replyBt.pack(pady=10)
    
    def addMention(self, user: str, comment: str) -> None:
        print(f"[!] Mention from @{user}: '{comment}'")
        notify(f"@{user} mentioned you", comment.replace("'", "'\\''"))

        self.mentions.insert("", tk.END, values=(user, comment))
    
    def onItemSelected(self, event) -> None:
        self.replyBt.config(state=tk.ACTIVE)
    
    def replyToMention(self) -> None:
        selectedItem = self.mentions.selection()
        if not selectedItem:
            return
        
        itemID = selectedItem[0]
        itemValues = self.mentions.item(itemID, "values")

        replyBox = ReplyBox(self.master, itemValues[0], self.levelID)
    
    def onClose(self) -> None:
        if messagebox.askyesno("Are you sure?", "Do you want to exit?"):
            self.master.destroy()
        else:
            return
