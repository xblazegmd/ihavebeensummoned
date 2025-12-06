import _tkinter
import glob
import logging
import os

from datetime import datetime
from gui import App
from utils import FORMATTER, LOGDIR

# Setup logging
logger = logging.getLogger("ihbs")
logger.setLevel(logging.DEBUG)

consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)
consoleHandler.setFormatter(FORMATTER)

# Setup log handler
logFile = LOGDIR / f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
logFile.parent.mkdir(parents=True, exist_ok=True)

fileHandler = logging.FileHandler(logFile, encoding="utf-8")
fileHandler.setLevel(logging.DEBUG)
fileHandler.setFormatter(FORMATTER)

logger.addHandler(consoleHandler)
logger.addHandler(fileHandler)

def main() -> None:
    # Look for older log files
    maxLogs = 10
    oldLogs = sorted(
        glob.glob(os.path.join(LOGDIR, "*.log")),
        key=os.path.getmtime
    )

    # Remove oldest log file
    if len(oldLogs) > maxLogs:
        for log in oldLogs[:-maxLogs]:
            os.remove(log)

    try:
        root = App()
        root.mainloop()
    except _tkinter.TclError as e:
        if "application has been destroyed" not in str(e):
            raise
        else:
            logger.warning("Tkinter's mad at you rn")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Exiting...")