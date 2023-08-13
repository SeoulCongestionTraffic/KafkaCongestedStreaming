"""
추상화 집단
"""
from typing import Any
from abc import ABC, abstractmethod
from core.setting.create_log import SocketLogCustomer


class AbstractAsyncResponseDataFactory(ABC):
    """
    Async Response Factory
    """

    @abstractmethod
    async def _xml_to_dict_convert(self, response: str) -> dict:
        """
        XML 문자열을 딕셔너리로 변환.

        Parameters:
        - xml_string (str): XML 형태의 문자열.

        Returns:
        - dict[str, Any]: XML을 딕셔너리로 변환한 결과.
        """
        raise NotImplementedError()

    @abstractmethod
    async def create_response(self, url: str) -> dict:
        """
        주어진 URL에 비동기 요청을 보내고 응답을 반환.

        Parameters:
        - url (str): API에 요청을 보낼 URL.

        Returns:
        - Any: XML 응답을 딕셔너리로 변환한 값.

        Raises:
        - RequestException: API 호출에 문제가 발생한 경우.
        """
        raise NotImplementedError()


class AbstractPlaceLocationClassifier(ABC):
    """
    Abstuact class for seoul place categori classfier
    """

    @abstractmethod
    def _get_english_category(self, korean_name: str):
        """
        한국어 -> 영어
        """
        raise NotImplementedError()

    @abstractmethod
    def place_classfier(self, filename: str):
        """
        지역별 코드 반환.

        Parameters:
        - filename (str): 지역별 코드가 저장된 CSV 파일의 경로. 기본값은 "config/seoul_place.csv".

        Returns:
        - dict[str, list[str]]: 카테고리별 지역 이름의 리스트를 값으로 하는 딕셔너리.
        """
        raise NotImplementedError()


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
    async def data_normalization(self, category: str, location: str) -> None:
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
    async def async_popular_congestion(self) -> None:
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
