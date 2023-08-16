"""
유틸 모음집
"""
from enum import Enum
from pathlib import Path
from datetime import datetime
from typing import Any, Union
from abc import abstractmethod

import time
import asyncio
import aiohttp
import xmltodict
import pandas as pd
from requests.exceptions import RequestException
from core.setting.create_log import SocketLogCustomer
from core.setting.properties import API_KEY, URL


class AsyncResponseDataFactory:
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
            await asyncio.sleep(1)
            match response.status:
                case 200:
                    return await self._xml_to_dict_convert(await response.text())
                case _:
                    raise RequestException(f"API 호출의 에러가 일어났습니다 --> {response.status}")


class SeoulPlaceClassifier:
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


class DataTransforFactor:
    """
    Abstuact class for seoul place kafka data factor
    """

    def __init__(self) -> None:
        self.logging = SocketLogCustomer()

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


def seoul_place() -> dict[str, list[str]]:
    """
    카테고리별 지역 반환 (서울)
    """
    return SeoulPlaceClassifier().place_classfier()


class CongestionLevel(Enum):
    """혼잡도 레벨 지정"""

    여유 = 0
    보통 = 1
    약간 = 2
    붐빔 = 3


def get_congestion_value(input_string: str) -> int:
    """혼잡도 레벨필터링"""
    if "약간" in input_string:
        return CongestionLevel.약간.value
    try:
        return CongestionLevel[input_string].value
    except KeyError:
        return 2


def utc_time(location_time: str) -> float:
    """utc time float transfor"""
    # 문자열을 datetime 객체로 변환
    date_time = datetime.strptime(location_time, "%Y-%m-%d %H:%M")

    # datetime 객체를 유닉스 타임스탬프로 변환
    return time.mktime(date_time.timetuple())


# 대문자 소문자 변환
def transform_data(obj):
    """
    대문자를 소문자로 재귀호출

    parameter
        - obj: dict or list comfact\n

    return:
    >>> {
        "area_name": "가로수길",
        "area_congestion_lvl": "보통",
        "area_congestion_msg": "사람이 몰려있을 수 있지만 크게 붐비지는 않아요. 도보 이동에 큰 제약이 없어요.",
        "area_ppltn_min": 30000,
        "area_ppltn_max": 32000,
        "fcst": "N",
        "age_congestion_specific": {
            "ppltn_rate_0": 0.3,
            "ppltn_rate_10": 5.7,
            "ppltn_rate_20": 26.9,
            "ppltn_rate_30": 26.4,
            "ppltn_rate_40": 18.9,
            "ppltn_rate_50": 11.7,
            "ppltn_rate_60": 6.3,
            "ppltn_rate_70": 3.7,
        },
    }

    """
    if isinstance(obj, list):
        return [transform_data(data) for data in obj]
    if isinstance(obj, dict):
        return _extracted_from_transform_data_32(obj, transform_data)
    return obj


def _extracted_from_transform_data_32(obj, transform_data):
    new_obj = {k.lower(): transform_data(v) for k, v in obj.items()}
    # fcst_ppltn_min 및 fcst_ppltn_max의 값을 실수로 변환
    if "fcst_ppltn_min" in new_obj:
        new_obj["fcst_ppltn_min"] = float(new_obj["fcst_ppltn_min"])
    if "fcst_ppltn_max" in new_obj:
        new_obj["fcst_ppltn_max"] = float(new_obj["fcst_ppltn_max"])
    if "fcst_time" in new_obj:
        new_obj["fcst_time"] = utc_time(new_obj["fcst_time"])
    if "fcst_congest_lvl" in new_obj:
        new_obj["fcst_congest_lvl"] = get_congestion_value(new_obj["fcst_congest_lvl"])
    return new_obj
