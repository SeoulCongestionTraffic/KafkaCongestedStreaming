"""
HTTP architecture 시작
"""
import aiohttp
from requests.exceptions import RequestException

from core.congestion.utils import XMLToDictConvertResponse
from core.setting.properties import API_KEY, URL


class AsyncResponseDataFactory:
    """
    Response Factory
    """

    def __init__(self) -> None:
        self.parsers = {"xml": XMLToDictConvertResponse()}

    async def create_response(self, url: str, response_type: str) -> dict:
        """
        주어진 URL에 비동기 요청을 보내고 응답을 반환.

        Parameters:
        - url (str): API에 요청을 보낼 URL.

        Returns:
        - Any: XML 응답을 딕셔너리로 변환한 값.

        Raises:
        - RequestException: API 호출에 문제가 발생한 경우.
        """
        parser = self.parsers.get(response_type)
        if not parser:
            raise ValueError(f"Unsupported response type: {response_type}")

        async with aiohttp.ClientSession() as session:
            response = await session.get(url)
            match response.status:
                case 200:
                    return await parser.xml_to_dict_convert(await response.text())
                case _:
                    raise RequestException(f"API 호출의 에러가 일어났습니다 --> {response.status}")


async def congestion(location: str, city_type: str = "citydata_ppltn") -> dict:
    """
    주어진 위치에 대한 혼잡도 정보를 비동기로 요청.

    Parameters:
    - location (str): 혼잡도 정보를 요청할 지역의 이름.

    Returns:
    - dict: 해당 위치의 혼잡도 정보.
    """
    url = f"{URL}/{API_KEY}/xml/{city_type}/1/1000/{location}"
    data = await AsyncResponseDataFactory().create_response(
        url=url, response_type="xml"
    )
    return data["Map"]["SeoulRtd.citydata_ppltn"]
