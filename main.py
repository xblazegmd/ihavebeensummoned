import _tkinter
import logging
from gui import App

# Setup logging
logger = logging.getLogger("ihbs")
logger.setLevel(logging.DEBUG)

consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    fmt="[%(asctime)s] %(levelname)s: %(message)s",
    datefmt="%H:%M:%S"
)
consoleHandler.setFormatter(formatter)

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