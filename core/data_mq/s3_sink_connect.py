import requests
import json

KAFKA_CONNECT_URL = "http://your-kafka-connect-url:8083"

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}

connector_config = {
    "name": "s3-sink-connector",
    "config": {
        "connector.class": "io.confluent.connect.s3.S3SinkConnector",
        "tasks.max": "1",
        "topics": "YOUR_TOPIC_NAME",
        "store.url": "s3://YOUR_BUCKET_NAME/log",
        "flush.size": "300",
        "format.class": "io.confluent.connect.s3.format.json.JsonFormat",
        "partitioner.class": "io.confluent.connect.storage.partitioner.DefaultPartitioner",
        "path.format": "'year'=YYYY/'month'=MM/'day'=dd",
        "locale": "en-US",
        "timezone": "UTC",
        "transforms": "routeTS,insertSource",
        "transforms.routeTS.type": "org.apache.kafka.connect.transforms.TimestampRouter",
        "transforms.routeTS.timestamp.format": "yyyy-MM-dd HH:mm:ss",
        "transforms.routeTS.topic.format": "${topic}/${timestamp}",
        # S3 인증 정보
        "s3.access.key": "YOUR_AWS_ACCESS_KEY",
        "s3.secret.key": "YOUR_AWS_SECRET_KEY",
        "s3.region": "YOUR_S3_REGION",  # 예: "us-west-1"
    },
}


response = requests.post(
    f"{KAFKA_CONNECT_URL}/connectors",
    headers=headers,
    data=json.dumps(connector_config),
    timeout=10,
)

print(response.json())
