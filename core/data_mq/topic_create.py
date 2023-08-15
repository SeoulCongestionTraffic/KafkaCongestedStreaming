"""
토픽생성
"""
from core.data_mq.data_admin import new_topic_initialization


from core.setting.properties import (
    DEVMKT_AGE,
    PALCULT_AGE,
    PARK_AGE,
    POPAREA_AGE,
    TOURZONE_AGE,
    AVG_DEVMKT_AGE,
    AVG_PALCULT_AGE,
    AVG_PARK_AGE,
    AVG_POPAREA_AGE,
    AVG_TOURZONE_AGE,
)
from core.setting.properties import (
    DEVMKT_NOF_AGE,
    PALCULT_NOF_AGE,
    PARK_NOF_AGE,
    POPAREA_NOF_AGE,
    TOURZONE_NOF_AGE,
    AVG_DEVMKT_NOF_AGE,
    AVG_PALCULT_NOF_AGE,
    AVG_PARK_NOF_AGE,
    AVG_POPAREA_NOF_AGE,
    AVG_TOURZONE_NOF_AGE,
)

from core.setting.properties import (
    DEVMKT_GENDER,
    PALCULT_GENDER,
    PARK_GENDER,
    POPAREA_GENDER,
    TOURZONE_GENDER,
    AVG_DEVMKT_GEN,
    AVG_PALCULT_GEN,
    AVG_PARK_GEN,
    AVG_POPAREA_GEN,
    AVG_TOURZONE_GEN,
)
from core.setting.properties import (
    DEVMKT_NOF_GENDER,
    PALCULT_NOF_GENDER,
    PARK_NOF_GENDER,
    POPAREA_NOF_GENDER,
    TOURZONE_NOF_GENDER,
    AVG_DEVMKT_NOF_GEN,
    AVG_PALCULT_NOF_GEN,
    AVG_PARK_NOF_GEN,
    AVG_POPAREA_NOF_GEN,
    AVG_TOURZONE_NOF_GEN,
)


def create_topic() -> None:
    """
    Topic create
    """
    topic = [
        DEVMKT_AGE,
        PALCULT_AGE,
        PARK_AGE,
        POPAREA_AGE,
        TOURZONE_AGE,
        DEVMKT_NOF_AGE,
        PALCULT_NOF_AGE,
        PARK_NOF_AGE,
        POPAREA_NOF_AGE,
        TOURZONE_NOF_AGE,
        DEVMKT_GENDER,
        PALCULT_GENDER,
        PARK_GENDER,
        POPAREA_GENDER,
        TOURZONE_GENDER,
        DEVMKT_NOF_GENDER,
        PALCULT_NOF_GENDER,
        PARK_NOF_GENDER,
        POPAREA_NOF_GENDER,
        TOURZONE_NOF_GENDER,
        AVG_DEVMKT_AGE,
        AVG_PALCULT_AGE,
        AVG_PARK_AGE,
        AVG_POPAREA_AGE,
        AVG_TOURZONE_AGE,
        AVG_DEVMKT_NOF_AGE,
        AVG_PALCULT_NOF_AGE,
        AVG_PARK_NOF_AGE,
        AVG_POPAREA_NOF_AGE,
        AVG_TOURZONE_NOF_AGE,
        AVG_DEVMKT_GEN,
        AVG_PALCULT_GEN,
        AVG_PARK_GEN,
        AVG_POPAREA_GEN,
        AVG_TOURZONE_GEN,
        AVG_DEVMKT_NOF_GEN,
        AVG_PALCULT_NOF_GEN,
        AVG_PARK_NOF_GEN,
        AVG_POPAREA_NOF_GEN,
        AVG_TOURZONE_NOF_GEN,
    ]
    partition: list[int] = [3 for _ in range(len(topic))]
    replication: list[int] = [3 for _ in range(len(topic))]

    return new_topic_initialization(
        topic=topic, partition=partition, replication_factor=replication
    )
