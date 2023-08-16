"""
async congestion
"""
import tracemalloc
from typing import Any, Type

from aiokafka.errors import KafkaConnectionError

from core.setting.properties import API_KEY, URL

from core.data_mq.data_interaction import produce_sending
from core.data_mq.topic_create import create_topic
from core.congestion_response.utils import seoul_place, DataTransforFactor
from core.congestion_response.abstract_class import (
    AbstractSeoulDataSending,
)
from core.congestion_response.data_format import (
    TotalAgeRateComposition as TRC,
    AreaGenderRateSpecific as AGRS,
)

tracemalloc.start()


class AsyncSeoulCongestionDataSending(AbstractSeoulDataSending):
    """Data Response"""

    def __init__(self, strategy: Type[DataTransforFactor]) -> None:
        super().__init__()
        self._strategy = strategy

    async def async_data_sending(
        self, congest: dict[str, Any], category: str, location: str, rate_type: str
    ) -> None:
        """데이터 전송 로직
        Args:
            - congest (dict[str, Any]): 혼잡도 데이터
            - category (str): 지역
            - location (str): 장소
            - rate_type (str): 혼잡도 타입
        """
        # 토픽명 변환 로직
        topic_transform = {
            "developed_market": "devMkt",
            "palace_and_cultural_heritage": "palCult",
            "park": "park",
            "populated_area": "popArea",
            "tourist_special_zone": "tourZone",
        }

        transformed_category = topic_transform.get(category, category)
        rate_schema: dict = self._strategy.transform(congest)
        try:
            match congest["FCST_YN"]:
                case "Y":
                    await produce_sending(
                        topic=f"{transformed_category}_{rate_type}",
                        message=rate_schema,
                        key=location,
                    )
                    await self.logging.data_log(
                        location=f"{transformed_category}_{rate_type}",
                        message=rate_schema,
                    )

                case "N":
                    await produce_sending(
                        topic=f"{transformed_category}_noF_{rate_type}",
                        message=rate_schema,
                        key=location,
                    )
                    await self.logging.data_log(
                        location=f"{transformed_category}_noF_{rate_type}",
                        message=rate_schema,
                    )

        except KafkaConnectionError as error:
            self.logging.error_log(
                error_type="kafka_connection", message=f"Kafk 데이터 전송 실패 --> {error}"
            )

    async def async_popular_congestion(self, rate_type: str) -> None:
        """혼잡도 데이터를 기반으로 적절한 토픽에 데이터를 전송

        매개변수:
            congest (dict[str, Any]): 혼잡도 데이터.
            category (str): 지역.
            location (str): 장소.
            rate_type (str): 혼잡도 타입.
        """
        create_topic()
        while True:
            try:
                for category, location in seoul_place().items():
                    await self.data_normalization(
                        category=category, location=location, rate_type=rate_type
                    )

            except KafkaConnectionError as error:
                await self.logging.error_log(error_type="NotConnection", message=error)
