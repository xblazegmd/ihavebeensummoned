import json
import os
import sys

from pathlib import Path
from typing import Any

from core.errors import*
from utils import logger

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
        try:
            json.dump(data, f, indent=4)
        except Exception as e:
            logger.error(f"Failed to save data to {SAVEFILE}: {e}")
            raise SFWriteError(f"Failed to save data to {SAVEFILE}") from e

def loadData() -> dict[Any, Any]:
    """
    Load the data from the save file and return it as a `dict`
    """
    if not os.path.exists(SAVEFILE):
        return {}
    
    with open(SAVEFILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            logger.error(f"Data in '{SAVEFILE}' is corrupted (error info: {e})")
            logger.info(f"Manual intervention is required")
            raise SFCorruptedError(f"Data in '{SAVEFILE}' is corrupted. Manual intervention is required") from e

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
