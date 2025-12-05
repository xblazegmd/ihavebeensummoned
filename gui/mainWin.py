import tkinter as tk
from tkinter import messagebox, ttk
from threading import Thread

from core.comments import commentListenerLoop
from core.errors import BoomlingsError
from utils import getDailyLevel, logger
from .devMode import DeveloperMode
from .listener import ListenerWindow

class MainWindow:
    def __init__(self, root: tk.Tk, devMode: bool) -> None:
        self.root = root
        self.devMode = devMode

        self.root.title("I have been summoned")
        self.root.geometry("300x200")
        self.root.resizable(False, False)

        self.label = ttk.Label(self.root, text="Getting daily level info...")
        self.button = ttk.Button(self.root, text="Start listener", state=tk.DISABLED, command=self.startListener)

        self.label.pack(pady=20)
        self.button.pack(pady=20)

        Thread(target=self.getDaily, daemon=True).start()
    
    def getDaily(self) -> None:
        if self.devMode:
            self.dailyID = "null_dev_mode"
            self.label.config(text="ID: null_dev_mode")
            self.button.config(state=tk.ACTIVE)
            return

        try:
            self.dailyID = getDailyLevel()
        
            self.label.config(text=f"ID: {self.dailyID}")
            self.button.config(state=tk.ACTIVE)
        except BoomlingsError as b:
            self.label.config(text=f"Error: {b}")
        except Exception as e:
            logger.error(str(e))
            messagebox.showerror("Error", "An unexpected error occurred. Plese report this issue to the GitHub, alongside the program's logs")
            self.label.config(text=f"Error: {e}")
    
    def startListener(self) -> None:
        listenerWindow = ListenerWindow(self.root, self.dailyID)
        listenerWindow.withdraw()
        
        devModeWin = None
        
        if self.devMode:
            devModeWin = DeveloperMode(self.root, listenerWindow.addMention)
            devModeWin.withdraw()
        else:
            Thread(target=commentListenerLoop, args=(self.dailyID, listenerWindow.addMention), daemon=True).start()

        if not self.devMode:
            self.button.config(text="Listener Running", state=tk.DISABLED)
            logger.info(f"Listener started on ID: {self.dailyID}")
            messagebox.showinfo("Listener started", f"Listener is currently running on ID: {self.dailyID}")

        self.root.withdraw()
        listenerWindow.deiconify()
        if devModeWin is not None:
            devModeWin.deiconify()
