"""
HTTP architecture 시작
"""
from pathlib import Path
from typing import Any

import aiohttp
import xmltodict
import pandas as pd
from requests.exceptions import RequestException

from congestion.setting.properties import API_KEY, URL


def get_english_topic(korean_topic):
    """
    토픽 매칭
    """
    topic_mapping = {
        "고궁·문화유산": "palace_and_cultural_heritage",
        "공원": "park",
        "관광특구": "tourist_special_zone",
        "발달상권": "developed_market",
        "인구밀집지역": "populated_area",
    }

    return topic_mapping.get(korean_topic, "unknown_topic")


def place_unique(filename: str = "setting/seoul_place.csv") -> dict[str, list[str]]:
    """
    지역별 코드 반환.

    Parameters:
    - filename (str): 지역별 코드가 저장된 CSV 파일의 경로. 기본값은 "setting/seoul_place.csv".

    Returns:
    - dict[str, list[str]]: 카테고리별 지역 이름의 리스트를 값으로 하는 딕셔너리.
    """
    csv_location = Path(__file__).parent
    place_data = pd.read_csv(f"{csv_location}/{filename}")

    return {
        get_english_topic(category): data["AREA_NM"].to_list()
        for category, data in place_data.groupby("CATEGORY")
    }


async def async_response_data(url: str) -> dict:
    """
    주어진 URL에 비동기 요청을 보내고 응답을 반환.

    Parameters:
    - url (str): API에 요청을 보낼 URL.

    Returns:
    - Any: XML 응답을 딕셔너리로 변환한 값.

    Raises:
    - RequestException: API 호출에 문제가 발생한 경우.
    """

    async def convert_xml_to_dict(xml_string: str) -> dict[str, Any]:
        """
        XML 문자열을 딕셔너리로 변환.

        Parameters:
        - xml_string (str): XML 형태의 문자열.

        Returns:
        - dict[str, Any]: XML을 딕셔너리로 변환한 결과.
        """
        return xmltodict.parse(xml_string)

    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        match response.status:
            case 200:
                return await convert_xml_to_dict(await response.text())
            case _:
                raise RequestException(f"API 호출의 에러가 일어났습니다 --> {response.status}")


async def congestion(location: str) -> dict:
    """
    주어진 위치에 대한 혼잡도 정보를 비동기로 요청.

    Parameters:
    - location (str): 혼잡도 정보를 요청할 지역의 이름.

    Returns:
    - dict: 해당 위치의 혼잡도 정보.
    """
    url = f"{URL}/{API_KEY}/xml/citydata_ppltn/1/1000/{location}"
    data = await async_response_data(url=url)
    return data["Map"]["SeoulRtd.citydata_ppltn"]


async def response_place():
    """
    호출
    """
    return place_unique()
