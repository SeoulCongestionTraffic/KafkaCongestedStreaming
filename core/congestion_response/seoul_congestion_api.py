"""
async congestion
"""
import asyncio
import tracemalloc
from typing import Any

from aiokafka.errors import KafkaConnectionError

from core.setting.properties import API_KEY, URL

from core.data_mq.data_interaction import produce_sending
from core.data_mq.topic_create import create_topic
from core.congestion_response.utils import seoul_place, AsyncResponseDataFactory
from core.congestion_response.abstract_class import AbstractSeoulDataSending
from core.congestion_response.data_format import (
    TotalAgeRateComposition as TRC,
)

tracemalloc.start()


class AsyncSeoulCongestionDataSending(AbstractSeoulDataSending):
    """Data Response"""

    async def async_congestion_response(
        self, location: str, city_type: str = "citydata_ppltn"
    ) -> dict[str, str] | dict[str, dict[str, str]]:
        """
        주어진 위치에 대한 혼잡도 정보를 비동기로 요청.

        Parameters:
        - location (str): 혼잡도 정보를 요청할 지역의 이름.

        Returns:
        - dict: 해당 위치의 혼잡도 정보.
        """
        url = f"{URL}/{API_KEY}/xml/{city_type}/1/1000/{location}"
        data = await AsyncResponseDataFactory().create_response(url=url)
        return data["Map"]["SeoulRtd.citydata_ppltn"]

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
        age_rate = TRC.schema_modify(congest)  # 고민
        match congest["FCST_YN"]:
            case "Y":
                await produce_sending(
                    topic=f"{category}_{rate_type}", message=age_rate, key=location
                )
            case "N":
                await produce_sending(
                    topic=f"{category}_not_FCST_YN_{rate_type}",
                    message=TRC.schema_modify(congest),
                    key=location,
                )

    async def data_normalization(self, category: str, location: str) -> None:
        """
        인구 혼잡도 kafka 연결
        - category: 지역
        - location: 장소
        """
        for data in location:
            congest = await self.async_congestion_response(data)
            # age_rate = TRC.schema_modify(congest)  # 고민
            # gender_rate = AGRS.schema_modify(congest)  # 고민
            await self.async_data_sending(
                congest=congest, category=category, location=data, rate_type="AGE"
            )
            await self.logging.data_log(location=category, message=congest)

    async def async_popular_congestion(self) -> None:
        """
        인구 혼잡도 kafka 연결
        """
        create_topic()
        while True:
            await asyncio.sleep(5)
            try:
                for category, location in seoul_place().items():
                    await self.data_normalization(category=category, location=location)

            except KafkaConnectionError as error:
                await self.logging.error_log(error_type="NotConnection", message=error)
