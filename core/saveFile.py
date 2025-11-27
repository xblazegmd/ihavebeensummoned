import json
import os
import sys

from pathlib import Path
from typing import Any

# For getting the root directory where to store the save file
# If running as an .app, default to ~/Library/Application Support/IHaveBeenSummoned
# If just running as "python main.py", default to where main.py is
def getRoot() -> Path:
    if getattr(sys, "frozen", False):
        root = Path.home() / "Library" / "Application Support" / "IHaveBeenSummoned"
    else:
        root = Path(sys.argv[0]).resolve().parent
    root.mkdir(parents=True, exist_ok=True)
    return root

SAVEFILE = getRoot() / "save.json"

def saveData(data: dict) -> None:
    """
    Overwrite the data in the save file with the new data
    
    WARNING: This will delete everything in the save file. For simple updates to the data, it's reccomended to use `updateData` instead.
    """
    with open(SAVEFILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def loadData() -> dict[Any, Any]:
    """
    Load the data from the save file and return it as a `dict`
    """
    if not os.path.exists(SAVEFILE):
        return {"nonexistent": True}
    
    with open(SAVEFILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {"corrupted": True} # Corrupted save file

def updateData(**kwargs) -> None:
    """
    Update the data in the save file.
    
    Unlike `saveData` which overwrites everything in the save file, `updateData` only updates the data in the save file without overwriting.
    This function is reccomended for most cases.

    The data to update must be passed as kwargs (keyword arguments)
    """
    current = loadData()
    for k, v in kwargs.items():
        current[k] = v
    saveData(current)
