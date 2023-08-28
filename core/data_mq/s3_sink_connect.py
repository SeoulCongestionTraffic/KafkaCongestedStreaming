import requests
import json
from core.setting.properties import (
    BOOTSTRAP_SERVER,
)
from core.setting.properties import (
    AVG_AGE_TOPIC,
    AVG_GENDER_TOPIC,
    AVG_N_AGE_TOPIC,
    AVG_N_GENDER_TOPIC,
    normal_topic_gender,
    normal_topic_age,
    normal_topic_no_age,
    normal_topic_no_gender,
)


def sink_connection(topics: list[str], name: str, tasks: str):
    KAFKA_CONNECT_URL = "http://localhost:8083"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    connector_config = {
        "name": f"s3-sink-connector-region-seoul-injection-{name}",
        "config": {
            "connector.class": "io.confluent.connect.s3.S3SinkConnector",
            "tasks.max": tasks,  # 병렬 처리를 위한 태스크 수
            "topics": topics,  # 콤마로 구분된 토픽 리스트
            "s3.bucket.name": "de-06-01-sparkcheckpointinstruction",
            "topics.dir": f"{name}",
            "s3.region": "ap-northeast-2",
            "flush.size": "300",  # S3에 쓰기 전에 버퍼에 쌓을 레코드 수
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

    return print(response.json())


topic_gender = sink_connection(
    topics=",".join(normal_topic_gender), name="nonmal_gender_pred", tasks=2
)
topic_no_gender = sink_connection(
    topics=",".join(normal_topic_no_gender), name="nonmal_gender", tasks=2
)

topic_age = sink_connection(
    topics=",".join(normal_topic_age), name="normal_age_pred", tasks=2
)
topic_no_age = sink_connection(
    topics=",".join(normal_topic_no_age), name="normal_age", tasks=2
)


avg_topic_age = sink_connection(topics=AVG_AGE_TOPIC, name="avg_topic_age", tasks=1)
avg_topic_gender = sink_connection(
    topics=AVG_GENDER_TOPIC, name="avg_topic_gender", tasks=1
)
avg_topic_n_age = sink_connection(
    topics=AVG_N_AGE_TOPIC, name="avg_topic_n_age", tasks=1
)
avg_topic_n_gender = sink_connection(
    topics=AVG_N_GENDER_TOPIC, name="avg_topic_n_gender", tasks=1
)
