"""
async congestion
"""
import asyncio
import tracemalloc

from aiokafka.errors import KafkaConnectionError

from core.setting.properties import API_KEY, URL
from core.data_mq.data_interaction import produce_sending
from core.data_mq.topic_create import create_topic
from core.congestion.abstract_class import AbstractSeoulDataSending
from core.congestion.utils import seoul_place, AsyncResponseDataFactory

tracemalloc.start()


class AsyncSeoulCongestionDataSending(AbstractSeoulDataSending):
    """Data Response"""

    async def congestion_response(
        self, location: str, city_type: str = "citydata_ppltn"
    ) -> dict:
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

    async def async_data_sending(self, category: str, location: str):
        """
        인구 혼잡도 kafka 연결
        - category: 지역
        - location: 장소
        """
        for data in location:
            congest = await self.congestion_response(data)
            await self.logging.data_log(location=category, message=congest)

            # 혼잡도 지표 제공 못할시 다른 토픽으로 이동
            if congest["FCST_YN"] == "N":
                await produce_sending(
                    topic=f"{category}_not_FCST_YN", message=congest, key=data
                )
            else:
                await produce_sending(topic=f"{category}", message=congest, key=data)

    async def async_popular_congestion(self):
        """
        인구 혼잡도 kafka 연결
        """
        create_topic()
        while True:
            await asyncio.sleep(5)
            try:
                for category, location in seoul_place().items():
                    await self.async_data_sending(category=category, location=location)

            except KafkaConnectionError as error:
                await self.logging.error_log(error_type="NotConnection", message=error)
