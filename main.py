import _tkinter
import logging
from gui import App

from utils import FORMATTER

# Setup logging
logger = logging.getLogger("ihbs")
logger.setLevel(logging.DEBUG)

consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)

consoleHandler.setFormatter(FORMATTER)

logger.addHandler(consoleHandler)

def main() -> None:
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