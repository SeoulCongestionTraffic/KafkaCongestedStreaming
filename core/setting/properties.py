"""
API에 필요한것들
"""
import sys
import configparser
from pathlib import Path


path = Path(__file__).parent.parent
parser = configparser.ConfigParser()
parser.read(f"{path}/config/setting.conf")

# 서울 API
API_KEY: str = parser.get("API", "key")
URL: str = parser.get("API", "url")

# KAFKA
BOOTSTRAP_SERVER: str = parser.get("KAFKA", "bootstrap_servers")
SECURITY_PROTOCOL: str = parser.get("KAFKA", "security_protocol")
MAX_BATCH_SIZE: int = parser.get("KAFKA", "max_batch_size")
ARCKS: str = parser.get("KAFKA", "acks")

# TOPIC
PALACE_AND_CULTURAL_HERITAGE: str = parser.get("TOPIC", "palace_and_cultural_heritage")
TOURIST_SPECIAL_ZONE: str = parser.get("TOPIC", "tourist_special_zone")
DEVELOPED_MARKET: str = parser.get("TOPIC", "developed_market")
POPULATED_AREA: str = parser.get("TOPIC", "populated_area")
PARK: str = parser.get("TOPIC", "park")

# TOPIC
DEVELOPED_MARKET_NOT_FCST_YN: str = parser.get("TOPIC", "developed_market_not_FCST_YN")
POPULATED_AREA_NOT_FCST_YN: str = parser.get("TOPIC", "populated_area_not_FCST_YN")
PARK_NOT_FCST_YN: str = parser.get("TOPIC", "park_not_FCST_YN")
PALACE_AND_CULTURAL_HERITAGE_NOT_FCST_YN: str = parser.get(
    "TOPIC", "palace_and_cultural_heritage_not_FCST_YN"
)
TOURIST_SPECIAL_ZONE_NOT_FCST_YN: str = parser.get(
    "TOPIC", "tourist_special_zone_not_FCST_YN"
)


# 메모리 계산
def deep_getsizeof(obj, seen=None) -> int:
    """재귀적으로 객체의 메모리 사용량을 계산하는 함수"""
    if seen is None:
        seen = set()

    obj_id = id(obj)
    if obj_id in seen:
        return 0

    # 이미 본 객체는 저장
    seen.add(obj_id)

    size = sys.getsizeof(obj)

    if isinstance(obj, dict):
        size += sum(deep_getsizeof(v, seen) for v in obj.values())
        size += sum(deep_getsizeof(k, seen) for k in obj.keys())
    elif hasattr(obj, "__iter__") and not isinstance(obj, (str, bytes, bytearray)):
        size += sum(deep_getsizeof(i, seen) for i in obj)

    return size
