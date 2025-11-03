import sys
import tkinter as tk
from tkinter import messagebox

from core.saveFile import saveData, loadData
from .mainWin import MainWindow
from .tagPrompt import TagPrompt
from .user import LoginWindow, PasswordPrompt

class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.withdraw()

        self.status = self.getStatus() # Temporary to test different login windows. -1 = First use + Login, 0 = Login, 1+ = Password check
        
        if self.status == 1:
            passPrompt = PasswordPrompt(self)
            self.wait_window(passPrompt)
        elif self.status == 0:
            loginWin = LoginWindow(self)
            self.wait_window(loginWin)
        elif self.status == -1:
            if not messagebox.askokcancel("I Have Been Summoned", "By using this program you are agreeing to Geometry Dash's Terms of Service, and our Privacy Policy (I went overkill with the legal stuff lol)"):
                self.destroy()
            loginWin = LoginWindow(self)
            self.wait_window(loginWin)
        
        data = loadData()
        if data.get("tags") is None:
            tagPrompt = TagPrompt(self)
            self.wait_window(tagPrompt)
        
        self.showMain()
    
    def showMain(self) -> None:
        self.deiconify()
        MainWindow(self)
    
    def getStatus(self) -> int:
        data = loadData()

        if data.get("nonexistent") is not None or data.get("corrupted") is not None:
            if data.get("corrupted") is not None and not messagebox.askyesno("Corrupted save file", "Your save file got corrupted. Do you want to generate a new one?"):
                sys.exit(0)
            saveData({}) # Initialize empty config file
            return -1
        
        if data.get("username") is None:
            return 0
        return 1
