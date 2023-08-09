"""
호출
"""

from core.setting.properties import API_KEY, URL
from core.congestion.utils import AsyncResponseDataFactory


async def congestion(location: str, city_type: str = "citydata_ppltn") -> dict:
    """
    주어진 위치에 대한 혼잡도 정보를 비동기로 요청.

    Parameters:
    - location (str): 혼잡도 정보를 요청할 지역의 이름.

    Returns:
    - dict: 해당 위치의 혼잡도 정보.
    """
    url = f"{URL}/{API_KEY}/xml/{city_type}/1/1000/{location}"
    data = await AsyncResponseDataFactory().create_response(url=url)
    return data["Map"]["SeoulRtd.citydata_ppltn"]
