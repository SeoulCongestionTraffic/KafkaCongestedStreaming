"""
API에 필요한것들
"""

import configparser
from pathlib import Path


path = Path(__file__).parent
parser = configparser.ConfigParser()
parser.read(f"{path}/setting.conf")

API_KEY: str = parser.get("API", "key")
URL: str = parser.get("API", "url")
