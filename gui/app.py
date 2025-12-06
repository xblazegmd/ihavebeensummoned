import os
import requests
import sys
import tkinter as tk
from tkinter import messagebox

from core.errors import *
from core.saveFile import saveData, loadData
from .mainWin import MainWindow
from .tagPrompt import TagPrompt
from .user import LoginWindow, PasswordPrompt
from utils import logger

class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.withdraw()

        # Basic internet check
        try:
            requests.get("https://www.google.com")
        except requests.ConnectionError:
            messagebox.showerror("Error", "No internet connection found. Please connect to the internet and try again")
            sys.exit(1)

        self.status = self.getStatus() # -2 = Developer mode, -1 = First use + Login, 0 = Login, 1+ = Password check
        self.devMode = False
        
        if self.status == 1:
            # User's already logged in, ask for password
            passPrompt = PasswordPrompt(self)
            self.wait_window(passPrompt)
        elif self.status == 0:
            # User's not logged in, log in
            loginWin = LoginWindow(self)
            self.wait_window(loginWin)
        elif self.status == -1:
            # User just started using the app, show disclaimer and log in
            if not messagebox.askokcancel("I Have Been Summoned", "By using this program you are agreeing to Geometry Dash's Terms of Service, and our Privacy Policy (I went overkill with the legal stuff lol)"):
                self.destroy()
            loginWin = LoginWindow(self)
            self.wait_window(loginWin)
        elif self.status == -2:
            # User's on developer mode
            self.devMode = True
        
        data = loadData()
        if data.get("tags") is None and not self.devMode:
            tagPrompt = TagPrompt(self)
            self.wait_window(tagPrompt)
        
        self.showMain()
    
    def showMain(self) -> None:
        self.deiconify()
        MainWindow(self, self.devMode)
    
    def getStatus(self) -> int:
        data = loadData()
        devMode = bool(data.get("devMode")) or bool(os.getenv("IHBS_DEV_MODE"))

        if devMode == True:
            return -2 # Developer mode: ON

        try:
            if data == {}:
                saveData({}) # Initialize empty file
                return -1
        
            if data.get("username") is None:
                return 0
            return 1
        except SFCorruptedError:
            if not messagebox.askyesno("Corrupted save file", "Your save file got corrupted. Do you want to generate a new one?"):
                sys.exit(0)
            
            saveData({}) # Reset data in save file
            return -1
