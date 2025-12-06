import logging
import requests
import sys
import subprocess
from tkinter import font, TclError
from tkinter.ttk import Label

from core import formatReq
from core.errors import *
from pathlib import Path

logger = logging.getLogger("ihbs")
FORMATTER = logging.Formatter(
    fmt="[%(asctime)s] %(levelname)s: %(message)s",
    datefmt="%H:%M:%S"
)

API = "http://www.boomlings.com/database/" # Yes, GD runs on boomlings.com
SECRET = "Wmfd2893gb7" # RobTop's secret key for server requests (that is not a secret anymore lol)
HEADERS = {"User-Agent": ""} # Empty User-Agent

# For getting the program's root directory in which to store the save files.
# If running as an .app, default to ~/Library/Application Support/IHaveBeenSummoned
# If just running as "python main.py", default to where main.py is
def getRootDir() -> Path:
    """
    For getting the program's root directory in which to store the save files.

    If running as an .app, default to `~/Library/Application Support/IHaveBeenSummoned`

    If just running as `python main.py`, default to where `main.py` is
    """
    if getattr(sys, "frozen", False):
        root = Path.home() / "Library" / "Application Support" / "IHaveBeenSummoned"
    else:
        root = Path(sys.argv[0]).resolve().parent
    root.mkdir(parents=True, exist_ok=True)
    return root

LOGDIR = getRootDir() / "logs"

def notify(title: str, message: str) -> None:
    """
    Send a notification.
    
    On MacOS notifications will get sent with `osascript`
    On Windows/Linux notifications will get sent with ___
    """
    subprocess.run(f"osascript -e 'display notification \"{message}\" with title \"{title}\"'", shell=True)

def getDailyLevel() -> str:
    """
    Get the current daily level
    idk how to get the daily with the ID "getGJDailyLevel" gives so I'm just gonna get it from the daily level's history (the vault)
    """
    params = {
        "type": 21, # Daily level history
        "secret": SECRET
    }

    # https://www.boomlings.com/database/getGJLevels21.php
    response = requests.post(API + "getGJLevels21.php", data=params, headers={"User-Agent": ""})

    if not (200 <= response.status_code < 300): # Not a success
        if response.status_code == 403:
            logger.error(f"Request to {API + 'getGJLevels21.php'} returned a 403 error")
            raise HTTPForbiddenError(f"Request to {API + 'getGJLevels21.php'} returned a 403 error")
        logger.error(f"Failed to get daily level info (status code: {response.status_code})")
        raise BoomlingsError(f"Failed to get daily level info (status code: {response.status_code})")
    
    # Format response
    daily = response.text.split("#")[0].split("|")[0] # TLDR; get the first level in the response

    dailyID = formatReq.formatKeyValuePairs(daily)["1"] # Get the level ID
    return dailyID

def changeFontSize(label: Label, size: int) -> font.Font:
    """
    Change the font size of a ttk Label
    """
    # Get the current font the label's using
    fntName = label.cget("font")
    try:
        fnt = font.nametofont(fntName)
    except TclError:
        fnt = font.Font(font=fntName)
    
    nfnt = fnt.copy() # Make a copy of it
    nfnt.configure(size=size) # Change the font size
    return nfnt

def setBold(label: Label) -> font.Font:
    """
    Make a ttk label **bold**
    """
    # Get the current font the label's using
    fntName = label.cget("font")
    try:
        fnt = font.nametofont(fntName)
    except TclError:
        fnt = font.Font(font=fntName)
    
    nfnt = fnt.copy() # Make a copy of it
    nfnt.configure(weight="bold") # Change the font size
    return nfnt