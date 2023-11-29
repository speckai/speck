import datetime
import os
import threading


def generate_metadata_dict() -> dict[str, str]:
    metadata: dict[str, str] = {
        "thread": threading.get_ident(),
        "process": os.getpid(),
        "timestamp": datetime.datetime.now(datetime.UTC).strftime(
            "%Y-%m-%d %H:%M:%S.%f"
        )[:-3],
    }
    return metadata
