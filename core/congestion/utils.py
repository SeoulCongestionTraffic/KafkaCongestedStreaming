"""
유틸 모음집
"""

from pathlib import Path

import xmltodict
import pandas as pd
from core.congestion.abstract_class import AbstractResponseParser


class XMLToDictConvertResponse(AbstractResponseParser):
    """
    Parses XML TO Dictionary responses.
    """

    async def xml_to_dict_convert(self, response: str) -> dict:
        """
        XML 문자열을 딕셔너리로 변환.

        Parameters:
        - xml_string (str): XML 형태의 문자열.

        Returns:
        - dict[str, Any]: XML을 딕셔너리로 변환한 결과.
        """
        return xmltodict.parse(response)


def place_unique(filename: str = "seoul_place.csv") -> dict[str, list]:
    """
    지역별 코드 반환.

    Parameters:
    - filename (str): 지역별 코드가 저장된 CSV 파일의 경로. 기본값은 "config/seoul_place.csv".

    Returns:
    - dict[str, list[str]]: 카테고리별 지역 이름의 리스트를 값으로 하는 딕셔너리.
    """

    def get_english_topic(korean_topic: str):
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

    csv_location = Path(__file__).parent.parent
    place_data = pd.read_csv(f"{csv_location}/config/{filename}")

    return {
        get_english_topic(category): data["AREA_NM"].to_list()
        for category, data in place_data.groupby("CATEGORY")
    }
