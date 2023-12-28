import datetime
import os
import threading
from typing import Any


def generate_metadata_dict() -> dict[str, Any]:
    metadata: dict[str, Any] = {
        "thread": threading.get_ident(),
        "process": os.getpid(),
        # "timestamp": datetime.datetime.now(datetime.UTC).strftime(
        #     "%Y-%m-%d %H:%M:%S.%f"
        # )[:-3],
        "timestamp": datetime.datetime.now().timestamp(),
    }
    return metadata
