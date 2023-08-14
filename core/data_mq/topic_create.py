"""
토픽생성
"""
from core.data_mq.data_admin import new_topic_initialization


from core.setting.properties import (
    PALACE_AND_CULTURAL_HERITAGE_AGE,
    TOURIST_SPECIAL_ZONE_AGE,
    DEVELOPED_MARKET_AGE,
    POPULATED_AREA_AGE,
    PARK_AGE,
)
from core.setting.properties import (
    PALACE_AND_CULTURAL_HERITAGE_NOT_FCST_AGE,
    TOURIST_SPECIAL_ZONE_NOT_FCST_AGE,
    DEVELOPED_MARKET_NOT_FCST_AGE,
    POPULATED_AREA_NOT_FCST_AGE,
    PARK_NOT_FCST_AGE,
)
from core.setting.properties import (
    PALACE_AND_CULTURAL_HERITAGE_GENDER,
    TOURIST_SPECIAL_ZONE_GENDER,
    DEVELOPED_MARKET_GENDER,
    POPULATED_AREA_GENDER,
    PARK_GENDER,
)
from core.setting.properties import (
    PALACE_AND_CULTURAL_HERITAGE_NOT_FCST_GENDER,
    TOURIST_SPECIAL_ZONE_NOT_FCST_GENDER,
    DEVELOPED_MARKET_NOT_FCST_GENDER,
    POPULATED_AREA_NOT_FCST_GENDER,
    PARK_NOT_FCST_GENDER,
)


def create_topic() -> None:
    """
    Topic create
    """
    topic = [
        PALACE_AND_CULTURAL_HERITAGE_AGE,
        TOURIST_SPECIAL_ZONE_AGE,
        DEVELOPED_MARKET_AGE,
        POPULATED_AREA_AGE,
        PARK_AGE,
        PALACE_AND_CULTURAL_HERITAGE_NOT_FCST_AGE,
        TOURIST_SPECIAL_ZONE_NOT_FCST_AGE,
        DEVELOPED_MARKET_NOT_FCST_AGE,
        POPULATED_AREA_NOT_FCST_AGE,
        PARK_NOT_FCST_AGE,
        PALACE_AND_CULTURAL_HERITAGE_NOT_FCST_GENDER,
        TOURIST_SPECIAL_ZONE_NOT_FCST_GENDER,
        DEVELOPED_MARKET_NOT_FCST_GENDER,
        POPULATED_AREA_NOT_FCST_GENDER,
        PARK_NOT_FCST_GENDER,
        PALACE_AND_CULTURAL_HERITAGE_GENDER,
        TOURIST_SPECIAL_ZONE_GENDER,
        DEVELOPED_MARKET_GENDER,
        POPULATED_AREA_GENDER,
        PARK_GENDER,
    ]
    partition: list[int] = [3 for _ in range(len(topic))]
    replication: list[int] = [3 for _ in range(len(topic))]

    return new_topic_initialization(
        topic=topic, partition=partition, replication_factor=replication
    )
