import os
import sys

sys.path.append((os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from speck import logger

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

with open(".env") as f:
    lines = f.readlines()
    for line in lines:
        key, value = line.split("=")
        os.environ[key] = value

SPECK_API_KEY = os.getenv("SPECK_API_KEY")

logger.app.set_api_key(SPECK_API_KEY)

logger.app.log("Testing 12")
