import tkinter as tk
from tkinter import ttk, messagebox

from core.saveFile import updateData
from utils import setBold

class TagPrompt(tk.Toplevel):
    def __init__(self, master, disabled: bool=False):
        super().__init__(master)
        self.disabled = disabled
        self.tags: list[str] = []

        self.title("Tags")
        self.geometry("350x250")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.onClose)

        # Main label
        label = ttk.Label(self, text="What tags should the program look for?")
        label.pack(pady=10)

        # Tags label
        self.tagsLabelVar = tk.StringVar()
        self.tagsLabelVar.set("No tags specified...")

        tagsLabel = ttk.Label(self, textvariable=self.tagsLabelVar)
        tagsLabel.configure(font=setBold(tagsLabel))
        tagsLabel.pack(pady=10)

        # Input to add tags
        # Frame
        frame = ttk.Frame(self)
        frame.pack()

        # Input
        self.tagsPrompt = ttk.Entry(frame)
        self.tagsPrompt.pack(side="left", fill="x")

        addBt = ttk.Button(frame, text="Add", width=1, command=self.addTag)
        addBt.pack(side="right")

        # Button to remove last element
        delBt = ttk.Button(self, text="Remove last element", command=self.removePrevTag)
        delBt.pack(pady=(30, 5))

        # Button to confirm
        confirmBt = ttk.Button(self, text="Confirm", command=self.setTags)
        confirmBt.pack(pady=5)
    
    def addTag(self) -> None:
        tag = self.tagsPrompt.get()
        self.tagsPrompt.delete(0, tk.END) # Empty the prompt

        # If the tag already exists, we don't need to add it again
        if tag in self.tags:
            messagebox.showerror("Error", "The specified tag is already in the list")
            return

        # Who's crazy enough to put only whitespace as a tag?
        if not tag.strip():
            messagebox.showerror("Are you crazy???", "Cannot add a space as a tag")
            return
        
        # Just whitespace overall is not the best for tags and stuff
        if any(c.isspace() for c in tag):
            # But we'll let the user add whitespace if they want for some reason
            if not messagebox.askyesno("Error", "Whitespace was found in the tag. It's not reccomended to put whitespace on a tag. Do you want to add it anyways?"):
                return
        
        self.tags.append(tag)

        self.tagsLabelVar.set(", ".join(self.tags)) # Show all tags separated by commas
    
    def removePrevTag(self) -> None:
        if not self.tags:
            messagebox.showerror("Error", "There's nothing to remove...")
            return # What are we gonna remove when there's nothing to remove?
        
        del self.tags[-1] # Remove last tag

        # Update the label too
        if not self.tags:
            self.tagsLabelVar.set("No tags specified...")
        else:
            self.tagsLabelVar.set(", ".join(self.tags))
    
    def setTags(self) -> None:
        if self.disabled:
            return

        if not messagebox.askokcancel("Tags", f"The tags will be set to: {', '.join(self.tags)}"):
            return
        updateData(tags=self.tags)
        self.destroy()
    
    def onClose(self) -> None:
        if self.disabled:
            self.destroy()
            return

        self.master.destroy()
