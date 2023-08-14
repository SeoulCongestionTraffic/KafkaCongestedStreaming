"""
추상화 집단
"""
from typing import Any
from abc import ABC, abstractmethod
from core.setting.create_log import SocketLogCustomer


class AbstractSeoulDataSending(ABC):
    """
    Abstuact class for seoul place kafka data sending
    """

    def __init__(self) -> None:
        self.logging = SocketLogCustomer()

    @abstractmethod
    async def async_congestion_response(
        self, location: str, city_type: str = "citydata_ppltn"
    ) -> dict:
        """
        주어진 위치에 대한 혼잡도 정보를 비동기로 요청.

        Parameters:
        - location (str): 혼잡도 정보를 요청할 지역의 이름.

        Returns:
        - dict: 해당 위치의 혼잡도 정보.
        """
        raise NotImplementedError()

    @abstractmethod
    async def data_normalization(
        self, category: str, location: str, rate_type: str
    ) -> None:
        """
        인구 혼잡도 kafka 연결
        - category: 지역
        - location: 장소
        """
        raise NotImplementedError()

    @abstractmethod
    async def async_data_sending(
        self, congest: dict[str, Any], category: str, location: str, rate_type: str
    ) -> None:
        """데이터 전송 로직

        Args:
            - congest (dict[str, Any]): 혼잡도 데이터
            - category (str): 지역
            - location (str): 장소
            - rate_type (str): 혼잡도 타입

        Raises:
            NotImplementedError: _description_
        """
        raise NotImplementedError()

    @abstractmethod
    async def async_popular_congestion(self, rate_type: str) -> None:
        """
        인구 혼잡도 kafka 연결
        """
        raise NotImplementedError()


class AbstractDataTransforFactor(ABC):
    """
    Abstuact class for seoul place kafka data factor
    """

    @abstractmethod
    def transform(self, data: dict[str, Any]) -> dict[str, Any]:
        """데이터 변환
        Args:
            data (dict[str, Any]):
                - 서울시 도시 데이터\n
        Returns:
            dict[str, Any]:
                - 변형된 스키마
        """
        raise NotImplementedError()
