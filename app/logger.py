import json
import logging
import logging.config
from pathlib import Path
import os

class PathFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        # Get path relative to the current working directory (project root)
        try:
            abs_path = Path(record.pathname).resolve()
            rel_path = abs_path.relative_to(Path.cwd().resolve())
            # Convert path parts or replace slashes to dot-notation (stripping .py extension optionally)
            clean_path = rel_path.with_suffix("")
            record.relpath = str(clean_path).replace(os.sep, ".").replace("/", ".")
        except ValueError:
            record.relpath = record.pathname
        return True

def setup_logging(config_path: str) -> Path:
    """Initializes logging configuration across the application from a JSON file."""
    log_dir = Path("./logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    
    path = Path(config_path)
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        print("could not find logger")
        logging.basicConfig(level=logging.INFO)
        
    return log_dir / "overwatch.log"