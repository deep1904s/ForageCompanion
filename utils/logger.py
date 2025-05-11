import os
import logging

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "foragecompanion32.log")

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_FILE, mode="w"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger("NotebookX")
