"""
location
"""

import json
import requests
import pandas as pd
import xmltodict
import time


def location_bus_drop_place() -> list:
    data = pd.read_excel("dd.xlsx")
    del data["번호"]

    return [i for i in data["장소명"]]


def xml_to_json(xml_string: requests):
    # XML 파싱하여 사전 형태로 변환
    xml_dict = xmltodict.parse(xml_string)

    return xml_dict


def ma_a():
    # url: str = f"http://openapi.seoul.go.kr:8088/5a58577451736b7936374968584359/xml/citydata/1/1000/노량진"
    url: str = f"http://openapi.seoul.go.kr:8088/5a58577451736b7936374968584359/xml/citydata_ppltn/1/1000/노량진"
    req = requests.get(url).text
    return xml_to_json(req)
