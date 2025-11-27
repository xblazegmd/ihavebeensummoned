import logging
import requests
import subprocess
from tkinter import font, TclError
from tkinter.ttk import Label

from core import formatReq

logger = logging.getLogger("ihbs")

API = "http://www.boomlings.com/database/" # Yes guys, GD runs on boomlings.com
SECRET = "Wmfd2893gb7" # RobTop's secret key for server requests (that is not a secret anymore lol)
HEADERS = {"User-Agent": ""} # Empty User-Agent

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
        logger.error(f"Failed to get daily level info (status code: {response.status_code})")
        return "-1" # Why the heck did I put "sys.exit(1)" before? What's wrong with me???
    
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