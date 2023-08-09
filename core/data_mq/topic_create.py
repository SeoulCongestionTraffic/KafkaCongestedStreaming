from core.data_mq.data_admin import new_topic_initialization


def create_topic() -> None:
    """
    Topic create
    """
    topic = [
        "palace_and_cultural_heritage",
        "park",
        "tourist_special_zone",
        "developed_market",
        "populated_area",
    ]
    partition = [3, 3, 3, 3, 3]
    replication = [3, 3, 3, 3, 3]

    return new_topic_initialization(
        topic=topic, partition=partition, replication_factor=replication
    )
