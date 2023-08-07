"""
TEST
"""
from typing import Any, Coroutine
from pathlib import Path

import asyncio
import aiohttp
from requests.exceptions import RequestException

import xmltodict
import pandas as pd
from setting.properties import API_KEY, URL


def csv_get_category(filename: str = "setting/seoul_place.csv") -> list[str]:
    """
    지역별 코드
    """
    excel_location = Path(__file__).parent
    data = pd.read_csv(f"{excel_location}/{filename}").groupby("CATEGORY")
    return list(pd.DataFrame(data=data)[0])


async def make_request_and_get_response(
    url: str,
) -> Coroutine[Any, Any, dict[str, Any]]:
    """
    TEST CODE
    """

    def convert_xml_to_dict(xml_string: str) -> dict[str, Any]:
        """
        TEST deco
        """
        return xmltodict.parse(xml_string)

    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        match response.status:
            case 200:
                return convert_xml_to_dict(await response.text())
            case _:
                raise RequestException(f"API 호출의 에러가 일어났습니다 --> {response.status}")


async def congestion(place: str):
    """
    TEST CODE
    """
    url = f"{URL}/{API_KEY}/xml/citydata/1/1000/{place}"
    data = await make_request_and_get_response(url)

    desired_columns = [
        "ROAD_TRAFFIC_STTS",
        # "ROAD_TRAFFIC_SPD",
        # "ROAD_TRAFFIC_IDX",
        # "ROAD_TRAFFIC_TIME",
        # "ROAD_MSG",
        # "LINK_ID",
        # "ROAD_NM",
        # "START_ND_CD",
        # "START_ND_NM",
        # "START_ND_XY",
        # "END_ND_CD",
        # "END_ND_NM",
        # "END_ND_XY",
        # "DIST",
        # "SPD",
        # "IDX",
    ]

    return data["SeoulRtd.citydata"]["CITYDATA"]["ROAD_TRAFFIC_STTS"]


if __name__ == "__main__":
    a = asyncio.run(congestion("노량진"))
    for i in a["ROAD_TRAFFIC_STTS"]:
        print(i)
