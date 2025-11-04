import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

import time

from threading import Thread
from typing import Callable

class DeveloperMode(tk.Toplevel):
    def __init__(self, master, onMention: Callable) -> None:
        super().__init__(master)
        self.onMention = onMention
        self.startTime = time.time()

        self.title("Developer Mode")
        self.geometry("550x300")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.onClose)

        # Debug labels
        version = ttk.Label(self, text="I Have Been Summoned v0.2-dev")
        version.pack(pady=5)

        self.uptime = ttk.Label(self, text="Uptime: 00:00:00")
        self.uptime.pack(pady=(0, 5))

        connectedFrame = ttk.Frame(self)
        connectedFrame.pack(pady=(0, 5))

        connectedLabel = ttk.Label(connectedFrame, text="Connected: null")
        connectedLabel.pack(side=tk.LEFT)

        connectedBt = ttk.Button(connectedFrame, text="Connect")
        connectedBt.pack(side=tk.RIGHT)

        # Logs
        self.logs = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=100, height=10, state=tk.DISABLED)
        self.logs.pack(pady=(0, 5))

        # Actions
        actionsFrame = ttk.Frame(self)
        actionsFrame.pack(pady=(0, 5))

        emulateBt = ttk.Button(actionsFrame, text="Emulate mention", command=self.emulateMention)
        emulateBt.pack(side=tk.LEFT, padx=5)

        promptBt = ttk.Button(actionsFrame, text="Open Prompt")
        promptBt.pack(side=tk.LEFT, padx=5)

        Thread(target=self.updateUptime, daemon=True).start()
        Thread(target=self.testUpdateLoop, daemon=True).start()

    def emulateMention(self) -> None:
        self.onMention("Example User", "This is just a test")

    def updateUptime(self) -> None:
        while True:
            self.uptime.config(text=f"Uptime: {self.getUptime()}")
            time.sleep(1)
    
    def getUptime(self) -> str:
        elapsed = time.time() - self.startTime
        h = int(elapsed // 3600)
        m = int((elapsed % 3600) // 60)
        s = int(elapsed % 60)
        return f"{h:02d}:{m:02d}:{s:02d}"

    def testUpdateLoop(self) -> None:
        while True:
            self.updateLogs()
            time.sleep(1)

    def updateLogs(self) -> None:
        self.logs.configure(state=tk.NORMAL)
        self.logs.insert(tk.END, f"[{self.getUptime()}] Log\n")
        self.logs.see(tk.END)
        self.logs.configure(state=tk.DISABLED)

    def onClose(self) -> None:
        if messagebox.askyesno("Are you sure?", "Do you want to exit?"):
            self.master.destroy()
        else:
            return
