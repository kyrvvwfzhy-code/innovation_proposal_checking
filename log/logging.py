import logging
import sys
from pathlib import Path

log_dir = Path.home() / "ipc"
log_dir.mkdir(parents = True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(log_dir / "IPC.log", encoding='utf-8')
    ]
)
logger = logging.getLogger("logs")
