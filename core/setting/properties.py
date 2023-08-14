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
MAX_REQUEST_SIZE: int = parser.get("KAFKA", "max_request_size")
ARCKS: str = parser.get("KAFKA", "acks")

# # TOPIC
# PALACE_AND_CULTURAL_HERITAGE: str = parser.get("TOPIC", "palace_and_cultural_heritage")
# TOURIST_SPECIAL_ZONE: str = parser.get("TOPIC", "tourist_special_zone")
# DEVELOPED_MARKET: str = parser.get("TOPIC", "developed_market")
# POPULATED_AREA: str = parser.get("TOPIC", "populated_area")
# PARK: str = parser.get("TOPIC", "park")

# # TOPIC
# DEVELOPED_MARKET_NOT_FCST: str = parser.get("TOPIC", "developed_market_not_FCST")
# POPULATED_AREA_NOT_FCST: str = parser.get("TOPIC", "populated_area_not_FCST")
# PARK_NOT_FCST: str = parser.get("TOPIC", "park_not_FCST")
# PALACE_AND_CULTURAL_HERITAGE_NOT_FCST: str = parser.get(
#     "TOPIC", "palace_and_cultural_heritage_not_FCST"
# )
# TOURIST_SPECIAL_ZONE_NOT_FCST: str = parser.get(
#     "TOPIC", "tourist_special_zone_not_FCST"
# )

# AGE TOPIC
PALACE_AND_CULTURAL_HERITAGE_AGE: str = parser.get(
    "AGETOPIC", "palace_and_cultural_heritage_AGE"
)
TOURIST_SPECIAL_ZONE_AGE: str = parser.get("AGETOPIC", "tourist_special_zone_AGE")
DEVELOPED_MARKET_AGE: str = parser.get("AGETOPIC", "developed_market_AGE")
POPULATED_AREA_AGE: str = parser.get("AGETOPIC", "populated_area_AGE")
PARK_AGE: str = parser.get("AGETOPIC", "park_AGE")

PARK_NOT_FCST_AGE: str = parser.get("AGETOPIC", "park_not_FCST_AGE")
DEVELOPED_MARKET_NOT_FCST_AGE: str = parser.get(
    "AGETOPIC", "developed_market_not_FCST_AGE"
)
POPULATED_AREA_NOT_FCST_AGE: str = parser.get("AGETOPIC", "populated_area_not_FCST_AGE")
PALACE_AND_CULTURAL_HERITAGE_NOT_FCST_AGE: str = parser.get(
    "AGETOPIC", "palace_and_cultural_heritage_not_FCST_AGE"
)
TOURIST_SPECIAL_ZONE_NOT_FCST_AGE: str = parser.get(
    "AGETOPIC", "tourist_special_zone_not_FCST_AGE"
)
# ------------------------------------------------------------------------------

# GENDER TOPIC
PALACE_AND_CULTURAL_HERITAGE_GENDER: str = parser.get(
    "GENDERTOPIC", "palace_and_cultural_heritage_GENDER"
)
TOURIST_SPECIAL_ZONE_GENDER: str = parser.get(
    "GENDERTOPIC", "tourist_special_zone_GENDER"
)
DEVELOPED_MARKET_GENDER: str = parser.get("GENDERTOPIC", "developed_market_GENDER")
POPULATED_AREA_GENDER: str = parser.get("GENDERTOPIC", "populated_area_GENDER")
PARK_GENDER: str = parser.get("GENDERTOPIC", "park_GENDER")

PARK_NOT_FCST_GENDER: str = parser.get("GENDERTOPIC", "park_not_FCST_GENDER")
DEVELOPED_MARKET_NOT_FCST_GENDER: str = parser.get(
    "GENDERTOPIC", "developed_market_not_FCST_GENDER"
)
POPULATED_AREA_NOT_FCST_GENDER: str = parser.get(
    "GENDERTOPIC", "populated_area_not_FCST_GENDER"
)
PALACE_AND_CULTURAL_HERITAGE_NOT_FCST_GENDER: str = parser.get(
    "GENDERTOPIC", "palace_and_cultural_heritage_not_FCST_GENDER"
)
TOURIST_SPECIAL_ZONE_NOT_FCST_GENDER: str = parser.get(
    "GENDERTOPIC", "tourist_special_zone_not_FCST_GENDER"
)
# ------------------------------------------------------------------------------


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


# 대문자 소문자 변환
def transform_data(obj):
    """
    대문자를 소문자로 재귀호출

    parameter
        - obj: dict or list comfact\n

    return:
    >>> {
        "area_name": "가로수길",
        "area_congestion_lvl": "보통",
        "area_congestion_msg": "사람이 몰려있을 수 있지만 크게 붐비지는 않아요. 도보 이동에 큰 제약이 없어요.",
        "area_ppltn_min": 30000,
        "area_ppltn_max": 32000,
        "fcst": "N",
        "age_congestion_specific": {
            "ppltn_rate_0": 0.3,
            "ppltn_rate_10": 5.7,
            "ppltn_rate_20": 26.9,
            "ppltn_rate_30": 26.4,
            "ppltn_rate_40": 18.9,
            "ppltn_rate_50": 11.7,
            "ppltn_rate_60": 6.3,
            "ppltn_rate_70": 3.7,
        },
    }

    """
    if isinstance(obj, list):
        return [transform_data(data) for data in obj]
    if isinstance(obj, dict):
        new_obj = {k.lower(): transform_data(v) for k, v in obj.items()}
        # fcst_ppltn_min 및 fcst_ppltn_max의 값을 실수로 변환
        if "fcst_ppltn_min" in new_obj:
            new_obj["fcst_ppltn_min"] = float(new_obj["fcst_ppltn_min"])
        if "fcst_ppltn_max" in new_obj:
            new_obj["fcst_ppltn_max"] = float(new_obj["fcst_ppltn_max"])
        return new_obj
    return obj
