import os
import threading
from datetime import datetime


def generate_metadata_dict():
    # Generate metadata for logs (based on thread, process, etc)
    metadata = {
        "thread": threading.get_ident(),
        "process": os.getpid(),
        "timestamp": datetime.now().isoformat(),
    }
    return metadata
