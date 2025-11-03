import tkinter as tk
from tkinter import messagebox, ttk
from threading import Thread

from core.comments import commentListenerLoop
from utils import getDailyLevel
from .listener import ListenerWindow

class MainWindow:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root

        self.root.title("I have been summoned")
        self.root.geometry("300x200")
        self.root.resizable(False, False)

        self.label = ttk.Label(self.root, text="Getting daily level info...")
        self.button = ttk.Button(self.root, text="Start listener", state=tk.DISABLED, command=self.startListener)

        self.label.pack(pady=20)
        self.button.pack(pady=20)

        Thread(target=self.getDaily, daemon=True).start()
    
    def getDaily(self) -> None:
        try:
            self.dailyID = getDailyLevel()
        
            self.label.config(text=f"ID: {self.dailyID}")
            self.button.config(text="Start Listener", state=tk.NORMAL)
        except Exception as e:
            self.label.config(text=f"Error: {e}")
    
    def startListener(self) -> None:
        listenerWindow = ListenerWindow(self.root, self.dailyID)
        listenerWindow.withdraw()
        
        Thread(target=commentListenerLoop, args=(self.dailyID, listenerWindow.addMention), daemon=True).start()

        self.button.config(text="Listener Running", state=tk.DISABLED)
        print(f"[+] Listener started on ID: {self.dailyID}")
        messagebox.showinfo("Listener started", f"Listener is currently running on ID: {self.dailyID}")

        self.root.withdraw()
        listenerWindow.deiconify()
