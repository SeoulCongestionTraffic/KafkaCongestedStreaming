"""
유틸 모음집
"""

from pathlib import Path

import aiohttp
import xmltodict
import pandas as pd
from requests.exceptions import RequestException

from core.congestion.abstract_class import (
    AbstractAsyncResponseDataFactory,
    AbstractPlaceLocationClassifier,
)


class AsyncResponseDataFactory(AbstractAsyncResponseDataFactory):
    """
    Response Factory
    """

    async def _xml_to_dict_convert(self, response: str) -> dict:
        """
        XML 문자열을 딕셔너리로 변환.

        Parameters:
        - xml_string (str): XML 형태의 문자열.

        Returns:
        - dict[str, Any]: XML을 딕셔너리로 변환한 결과.
        """
        return xmltodict.parse(response)

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
        async with aiohttp.ClientSession() as session:
            response = await session.get(url)
            match response.status:
                case 200:
                    return await self._xml_to_dict_convert(await response.text())
                case _:
                    raise RequestException(f"API 호출의 에러가 일어났습니다 --> {response.status}")


class SeoulPlaceClassifier(AbstractPlaceLocationClassifier):
    """
    카테고리 <---> 지역 매칭
    확장성 고려
    """

    def __init__(self) -> None:
        self.csv_location: Path = Path(__file__).parent.parent

    def _get_english_category(self, korean_name: str) -> str:
        category_mapping = {
            "고궁·문화유산": "palace_and_cultural_heritage",
            "공원": "park",
            "관광특구": "tourist_special_zone",
            "발달상권": "developed_market",
            "인구밀집지역": "populated_area",
        }

        return category_mapping.get(korean_name, "unknown_topic")

    def place_classfier(
        self, filename: str = "seoul_place.csv"
    ) -> dict[str, list[str]]:
        """
        카테고리별 지역 반환

        Parameters:
        - filename (str): 카테고리 와 지역이 저장된 CSV 파일의 경로. 기본값은 "config/seoul_place.csv".

        Returns:
        - dict[str, list[str]]: 카테고리별 지역 이름의 리스트를 값으로 하는 딕셔너리.
        """
        place_data = pd.read_csv(f"{self.csv_location}/config/{filename}")

        return {
            self._get_english_category(category): data["AREA_NM"].to_list()
            for category, data in place_data.groupby("CATEGORY")
        }


def seoul_place() -> dict[str, list[str]]:
    """
    카테고리별 지역 반환 (서울)
    """
    return SeoulPlaceClassifier().place_classfier()
