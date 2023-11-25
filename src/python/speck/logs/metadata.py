import os
import threading
from datetime import datetime


def generate_metadata_dict() -> dict[str, str]:
    metadata: dict[str, str] = {
        "thread": threading.get_ident(),
        "process": os.getpid(),
        "timestamp": datetime.utcnow().isoformat(),
    }
    return metadata
