import random
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog

import logging
import os
import sys
import subprocess
import time
from threading import Thread
from typing import Callable

from core.comments import commentListenerLoop
from core.devModeLogHandler import DevModeLogHandler
from core.saveFile import SAVEFILE
from gui.listener import ListenerWindow
from .prompts import Prompts
from utils import logger, notify, getDailyLevel

class DeveloperMode(tk.Toplevel):
    def __init__(self, master, onMention: Callable) -> None:
        super().__init__(master)
        self.onMention = onMention
        self.startTime = time.time()
        self.connected = None

        self.title("Developer Mode")
        self.geometry("550x300")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.onClose)

        # Debug labels
        version = ttk.Label(self, text="I Have Been Summoned v0.2-dev")
        version.pack(pady=5)

        self.uptime = ttk.Label(self, text="Uptime: 00:00:00")
        self.uptime.pack(pady=(0, 5))

        connected = ttk.Label(self, text=f"Connected: {self.connected}")
        connected.pack(pady=(0, 5))

        # Logs
        self.logs = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=100, height=10, state=tk.DISABLED)
        self.logs.pack(pady=(0, 5))

        # Log styling
        self.logs.tag_config("WARNING", foreground="yellow")
        self.logs.tag_config("ERROR", foreground="red")
        self.logs.tag_config("CRITICAL", foreground="red", underline=True)

        # Setup logging
        self.logHandler = DevModeLogHandler(self.log)
        self.logHandler.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            fmt="[%(asctime)s] %(levelname)s: %(message)s",
            datefmt="%H:%M:%S"
        )
        self.logHandler.setFormatter(formatter)
        
        logger.addHandler(self.logHandler)

        # Actions
        actions = ttk.Frame(self)
        actions.pack(pady=(0, 5))

        emulateBt = ttk.Button(actions, text="Emulate mention", width=12, command=self.emulateMention)
        emulateBt.grid(row=0, column=0)

        promptBt = ttk.Button(actions, text="Open Prompt", width=12, command=self.openPrompt)
        promptBt.grid(row=0, column=1)

        connectBt = ttk.Button(actions, text="Connect to level", width=12, command=self.connectToLevel)
        connectBt.grid(row=0, column=2)

        configBt = ttk.Button(actions, text="Configuration", width=12, command=self.openConfig)
        configBt.grid(row=1, column=0)

        self.eventlogBt = ttk.Button(actions, text="Disable logging", width=12, command=self.toggleLogs)
        self.eventlogBt.grid(row=1, column = 1)
        
        reloadBt = ttk.Button(actions, text="Restart", width=12, command=self.restart)
        reloadBt.grid(row=1, column=2)

        Thread(target=self.updateUptime, daemon=True).start()

    def emulateMention(self) -> None:
        # Username generation
        pre = [
            "Clubstep",
            "RobTop",
            "Amazing",
            "Xblaze",
            "TheReal",
            "Vector",
            "Fingerdash",
            "Deadlocked",
            "Electroman",
            "Extreme",
            "Demon"
        ]
        suf = [
            "Fanatic",
            "Dasher",
            "Lover",
            "Bean",
            "X",
            "XD",
            "Slayer",
            "CantLetGo",
            "NonSense",
            "Step",
            "Woah",
            "Demon",
            "What"
        ]
        username = random.choice(pre) + random.choice(suf) + str(random.randint(0, 5000))

        # Random message
        msgs = [
            "how are you?",
            "truth or dare",
            "how was your day?",
            "lol",
            "really?",
            "idrk",
            "what",
            "xd",
            "im fine, wbu?",
            "woah",
            "there's no way that's true",
            "WHAT",
            "are you ok?",
            "i can't believe it!",
            "IKR ;-;",
            ";-;",
            "ToT",
            ":)",
            ">:)",
            "uhm...",
            "heck no",
            "screw you",
            "no u",
            "uno reverse"
        ]

        msg = random.choice(msgs)
        logger.info(f"Mention by {username}: {msg}")
        notify(f"@{username} mentioned you", msg.replace("'", "'\\''"))

        self.onMention(username, random.choice(msg))

    def openPrompt(self) -> None:
        Prompts(self.master)
    
    def connectToLevel(self) -> None:
        if self.connected is not None:
            logger.error(f"Already connected to level ID: {self.connected}")
            messagebox.showerror("Error", f"Already connected to level ID: {self.connected}")
            return

        levelID = simpledialog.askstring("Connect to level", "Enter level ID (-1: Daily):", parent=self)
        if levelID is None:
            logger.error("No level ID provided.")
            messagebox.showerror("Error", "No level ID provided.")
            return

        logger.debug(f"Level ID: {levelID}")

        if levelID == "-1":
            logger.debug("Fetching daily level ID")
            levelID = getDailyLevel()
            if levelID == "-1":
                messagebox.showerror("Error", "Failed to get daily level ID.")
                return
            
            logger.debug(f"Daily level ID: {levelID}")

        self.connected = levelID

        Thread(target=commentListenerLoop, args=(levelID, self.onMention), daemon=True).start()

        logger.info(f"Listener started on ID: {levelID}")
        messagebox.showinfo("Listener started", f"Listener is currently running on ID: {levelID}")
    
    def openConfig(self) -> None:
        subprocess.Popen(["open", str(SAVEFILE)])
    
    def toggleLogs(self) -> None:
        disabled = not logger.disabled

        self.eventlogBt.config(text="Enable logging" if disabled else "Disable logging")

        # So the "LOGS: ____" message works I need to check the state before and after changing it
        # This is checked before since it won't log after
        if disabled:
            logger.info("Logging: DISABLED")
        
        logger.disabled = disabled

        # This is checked after since it won't log before
        if not disabled:
            logger.info("Logging: ENABLED")
    
    def restart(self) -> None:
        if not messagebox.askyesno(
            title="Are you sure?",
            message="Do you want to restart the application?"
        ):
            return
        
        exe = sys.executable
        os.execv(exe, [exe] + sys.argv)

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

    def log(self, msg: str, level: str="DEBUG") -> None:
        self.logs.configure(state=tk.NORMAL)
        self.logs.insert(tk.END, msg + "\n", (level,))
        self.logs.see(tk.END)
        self.logs.configure(state=tk.DISABLED)

    def onClose(self) -> None:
        if messagebox.askyesno("Are you sure?", "Do you want to exit?"):
            self.master.destroy()
        else:
            return
