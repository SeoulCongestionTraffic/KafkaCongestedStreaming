"""
TEST API 분석
"""
from pathlib import Path
from typing import Any

import requests
import xmltodict
import pandas as pd
from requests.exceptions import RequestException
from setting.properties import API_KEY, URL


def excel_get_locations(filename: str = "setting/place.xlsx") -> list[str]:
    """
    TEST CODE
    """
    excel_location = Path(__file__).parent
    return list(pd.read_excel(f"{excel_location}/{filename}")["장소명"])


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


if __name__ == "__main__":
    from contextlib import suppress

    with suppress(KeyError):
        for plcae in excel_get_locations():
            print(congestion(place=plcae)["Map"]["SeoulRtd.citydata_ppltn"])
