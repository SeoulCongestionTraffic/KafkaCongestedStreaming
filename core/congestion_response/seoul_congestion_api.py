"""
async congestion
"""
import asyncio
import tracemalloc
from typing import Any, Union, Type

from aiokafka.errors import KafkaConnectionError
from requests.exceptions import RequestException

from core.setting.properties import API_KEY, URL

from core.data_mq.data_interaction import produce_sending
from core.data_mq.topic_create import create_topic
from core.congestion_response.utils import seoul_place, AsyncResponseDataFactory
from core.congestion_response.abstract_class import (
    AbstractSeoulDataSending,
    AbstractDataTransforFactor,
)
from core.congestion_response.data_format import (
    TotalAgeRateComposition as TRC,
    AreaGenderRateSpecific as AGRS,
)

tracemalloc.start()


class AsyncSeoulCongestionDataSending(AbstractSeoulDataSending):
    """Data Response"""

    def __init__(self, strategy: Type[AbstractDataTransforFactor]) -> None:
        super().__init__()
        self._strategy = strategy

    async def async_congestion_response(
        self, location: str, city_type: str = "citydata_ppltn"
    ) -> dict[str, Union[str, dict[str, list[str]]]]:
        """
        주어진 위치에 대한 혼잡도 정보를 비동기로 요청

        매개변수:
            location (str): 혼잡도 정보를 요청할 지역의 이름.
            city_type (str, optional): 도시 데이터 타입. 기본값은 "citydata_ppltn".

        반환값:
            dict[str, Union[str, dict[str, list[str, str]]]: 지정된 위치의 혼잡도 정보.
        """
        try:
            url = f"{URL}/{API_KEY}/xml/{city_type}/1/1000/{location}"
            data: dict = await AsyncResponseDataFactory().create_response(url=url)
            return data["Map"]["SeoulRtd.citydata_ppltn"]
        except RequestException as error:
            self.logging.error_log(
                error_type="connection_error", message=f"데이터 요청 중 오류 발생: {error}"
            )
            return {}

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
        rate_schema: dict = self._strategy.transform(congest)
        try:
            match congest["FCST_YN"]:
                case "Y":
                    await produce_sending(
                        topic=f"{category}_{rate_type}",
                        message=rate_schema,
                        key=location,
                    )
                case "N":
                    await produce_sending(
                        topic=f"{category}_not_FCST_YN_{rate_type}",
                        message=rate_schema,
                        key=location,
                    )
        except KafkaConnectionError as error:
            self.logging.error_log(
                error_type="kafka_connection", message=f"Kafk 데이터 전송 실패 --> {error}"
            )

    async def data_normalization(
        self, category: str, location: str, rate_type: str
    ) -> None:
        """
        인구 혼잡도 kafka 연결
        - category: 지역
        - location: 장소
        """
        for data in location:
            congest = await self.async_congestion_response(data)
            await self.async_data_sending(
                congest=congest, category=category, location=data, rate_type=rate_type
            )
            await self.logging.data_log(location=category, message=congest)

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
            await asyncio.sleep(5)
            try:
                for category, location in seoul_place().items():
                    await self.data_normalization(
                        category=category, location=location, rate_type=rate_type
                    )

            except KafkaConnectionError as error:
                await self.logging.error_log(error_type="NotConnection", message=error)


class AgeCongestionRate(AbstractDataTransforFactor):
    """나이별 혼잡도 클래스"""

    def transform(self, data: dict[str, Any]) -> dict[str, Any]:
        return TRC.schema_modify(data)


class GenderCongestionRate(AbstractDataTransforFactor):
    """성별 혼잡도 클래스"""

    def transform(self, data: dict[str, Any]) -> dict[str, Any]:
        return AGRS.schema_modify(data)
