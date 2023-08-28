import requests
import json
from core.setting.properties import (
    BOOTSTRAP_SERVER,
)
from core.setting.properties import (
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
)

from core.setting.properties import (
    DEVMKT_NOF_GENDER,
    PALCULT_NOF_GENDER,
    PARK_NOF_GENDER,
    POPAREA_NOF_GENDER,
    TOURZONE_NOF_GENDER,
    DEVMKT_GENDER,
    PALCULT_GENDER,
    PARK_GENDER,
    POPAREA_GENDER,
    TOURZONE_GENDER,
)
from core.setting.properties import (
    AVG_AGE_TOPIC,
    AVG_GENDER_TOPIC,
    AVG_N_AGE_TOPIC,
    AVG_N_GENDER_TOPIC,
)


def sink_connection():
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
        AVG_AGE_TOPIC,
        AVG_GENDER_TOPIC,
        AVG_N_AGE_TOPIC,
        AVG_N_GENDER_TOPIC,
    ]

    KAFKA_CONNECT_URL = "http://localhost:8083"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    connector_config = {
        "name": "s3-sink-connector-region-seoul-injection-00107",
        "config": {
            "connector.class": "io.confluent.connect.s3.S3SinkConnector",
            "tasks.max": "1",  # 병렬 처리를 위한 태스크 수
            "topics": ",".join(topic),  # 콤마로 구분된 토픽 리스트
            "s3.bucket.name": "de-06-01-sparkcheckpointinstruction",
            "s3.region": "ap-northeast-2",
            "flush.size": "100",  # S3에 쓰기 전에 버퍼에 쌓을 레코드 수
            "storage.class": "io.confluent.connect.s3.storage.S3Storage",
            "format.class": "io.confluent.connect.s3.format.json.JsonFormat",
            "key.converter": "org.apache.kafka.connect.storage.StringConverter",
            "value.converter": "org.apache.kafka.connect.storage.StringConverter",
            "partitioner.class": "io.confluent.connect.storage.partitioner.TimeBasedPartitioner",
            "path.format": "YYYY/MM/dd/HH",
            "locale": "ko-KR",
            "timezone": "UTC",
            "schemas.enable": False,
            "partition.duration.ms": 60000,
            "bootstrap.servers": BOOTSTRAP_SERVER,
        },
    }

    response = requests.post(
        f"{KAFKA_CONNECT_URL}/connectors",
        headers=headers,
        data=json.dumps(connector_config),
        timeout=10,
    )

    print(response.json())
