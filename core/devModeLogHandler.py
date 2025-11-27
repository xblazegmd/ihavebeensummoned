import logging
from typing import Callable

class DevModeLogHandler(logging.Handler):
    def __init__(self, callback: Callable) -> None:
        super().__init__()
        self.callback = callback
    
    def emit(self, record: logging.LogRecord) -> None:
        level = "NOTSET"
        match record.levelno:
            case logging.DEBUG:
                level = "DEBUG"
            case logging.INFO:
                level = "INFO"
            case logging.WARNING:
                level = "WARNING"
            case logging.ERROR:
                level = "ERROR"
            case logging.CRITICAL:
                level = "CRITICAL"

        msg = self.format(record)
        self.callback(msg, level)