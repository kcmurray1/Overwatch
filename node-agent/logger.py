import logging
import logging.config
from datetime import datetime
from pathlib import Path
import uuid
def setup_logging(logfile_name: str= None, prepend_timestamp: bool=False) -> Path:
    """Initializes logging configuration across the application."""
    log_dir = Path("./logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if not logfile_name:
        logfile_name = f"run_{uuid.uuid4()}"
        
    if prepend_timestamp:
        logfile_name = timestamp + logfile_name
    
        
    log_file_path = log_dir / f"{logfile_name}.log"

    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "console_fmt": {
                "format": "[%(levelname)s] [%(name)s] %(message)s"
            },
            "file_fmt": {
                "format": "%(asctime)s [%(name)s] - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "console_fmt",
                "stream": "ext://sys.stdout",
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "DEBUG",
                "formatter": "file_fmt",
                "filename": str(log_file_path),
                "maxBytes": 5 * 1024 * 1024,  # 5 MB
                "backupCount": 3,
                "encoding": "utf-8",
            },
        },
        "root": {
            "level": "DEBUG",
            "handlers": ["console", "file"]
        },
    }
    logging.config.dictConfig(LOGGING_CONFIG)
    return log_file_path

def get_logger(module_name: str) -> logging.Logger:
    """Gets a child logger for a specific module under character_clipper."""
    return logging.getLogger(module_name)