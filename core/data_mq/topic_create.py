"""
토픽생성
"""
from core.data_mq.data_admin import new_topic_initialization
from core.setting.properties import (
    PALACE_AND_CULTURAL_HERITAGE,
    TOURIST_SPECIAL_ZONE,
    DEVELOPED_MARKET,
    POPULATED_AREA,
    PARK,
)
from core.setting.properties import (
    PALACE_AND_CULTURAL_HERITAGE_NOT_FCST_YN,
    TOURIST_SPECIAL_ZONE_NOT_FCST_YN,
    DEVELOPED_MARKET_NOT_FCST_YN,
    POPULATED_AREA_NOT_FCST_YN,
    PARK_NOT_FCST_YN,
)


def create_topic() -> None:
    """
    Topic create
    """
    topic = [
        PALACE_AND_CULTURAL_HERITAGE,
        TOURIST_SPECIAL_ZONE,
        DEVELOPED_MARKET,
        POPULATED_AREA,
        PARK,
        PALACE_AND_CULTURAL_HERITAGE_NOT_FCST_YN,
        TOURIST_SPECIAL_ZONE_NOT_FCST_YN,
        DEVELOPED_MARKET_NOT_FCST_YN,
        POPULATED_AREA_NOT_FCST_YN,
        PARK_NOT_FCST_YN,
    ]
    partition = [3 for _ in range(len(topic))]
    replication = [3 for _ in range(len(topic))]

    return new_topic_initialization(
        topic=topic, partition=partition, replication_factor=replication
    )
