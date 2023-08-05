"""
TEST API 분석
"""
import configparser
from pathlib import Path
from typing import Any

import requests
import xmltodict
import pandas as pd
from requests.exceptions import RequestException


path = Path(__file__).parent.parent
parser = configparser.ConfigParser()
parser.read(f"{path}/setting/setting.conf")
key: str = parser.get("api", "key")


def excel_get_locations(filename: str = "dd.xlsx") -> list[str]:
    """
    TEST CODE
    """
    data = pd.read_excel(filename)
    del data["번호"]
    return list(data["장소명"])


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


def main():
    """
    TEST CODE
    """
    url = f"http://openapi.seoul.go.kr:8088/{key}/xml/citydata_ppltn/1/1000/구로디지털단지역"
    get_response = make_request_and_get_response(url)
    print(get_response)


if __name__ == "__main__":
    main()
