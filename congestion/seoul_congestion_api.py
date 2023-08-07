"""
HTTP architecture 시작
"""
from pathlib import Path
from typing import Any

import requests
import xmltodict
import pandas as pd
from requests.exceptions import RequestException
from setting.properties import API_KEY, URL


def csv_get_locations(filename: str = "setting/seoul_place.csv") -> list[str]:
    """
    지역별 코드
    """
    excel_location = Path(__file__).parent
    place_data = pd.read_csv(f"{excel_location}/{filename}").groupby("CATEGORY")
    return list(place_data)


def make_request_and_get_response(url: str) -> Any:
    """
    TEST CODE
    """

    def convert_xml_to_dict(xml_string: str) -> dict[str, Any]:
        """
        TEST deco
        """
        return xmltodict.parse(xml_string)

    response = requests.get(url, timeout=10)
    match response.status_code:
        case 200:
            return convert_xml_to_dict(response.text)
        case _:
            raise RequestException(f"API 호출의 에러가 일어났습니다 --> {response.status_code}")


def congestion(place: str):
    """
    TEST CODE
    """
    url = f"{URL}/{API_KEY}/xml/citydata_ppltn/1/1000/{place}"
    return make_request_and_get_response(url)
