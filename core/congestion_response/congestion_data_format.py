"""
필요한 데이터스키마 나누기
"""
import logging
from pydantic import BaseModel, ValidationError, field_validator


class TotalAgeRate(BaseModel):
    """나이 연령별 묶음"""

    area_name: str
    area_congestion_lvl: str
    area_congestion_msg: str
    area_ppltn_min: int
    area_ppltn_max: int


class AgeCongestionSpecific(BaseModel):
    """나이대 별 혼잡도"""

    ppltn_rate_0: float
    ppltn_rate_10: float
    ppltn_rate_20: float
    ppltn_rate_30: float
    ppltn_rate_40: float
    ppltn_rate_50: float
    ppltn_rate_60: float
    ppltn_rate_70: float


class TotalAgeRateComposition(TotalAgeRate):
    """나이대 별 혼잡도 Customizer"""

    age_congestion_specific: AgeCongestionSpecific

    @field_validator("age_congestion_specific", mode="plain", check_fields=True)
    @classmethod
    def _ppltn_data(cls, data: dict[str, str]) -> AgeCongestionSpecific:
        """
        인구 rate 추출

        Args:
            data (dict[str, str]): 서울시 인구 혼잡도 dictionary
                >>> a = {
                    "AREA_NM": "가로수길",
                    "AREA_CD": "POI059",
                    "AREA_CONGEST_LVL": "보통",
                    "AREA_CONGEST_MSG": "사람이 몰려있을 수 있지만 크게 붐비지는 않아요. 도보 이동에 큰 제약이 없어요.",
                    "AREA_PPLTN_MIN": "30000",
                    "AREA_PPLTN_MAX": "32000",
                    ...
                }
        Returns:
            >>> "age_congestion_specific": {
                "ppltn_rate_0": 0.3,
                "ppltn_rate_10": 5.7,
                "ppltn_rate_20": 26.9,
                "ppltn_rate_30": 26.4,
                "ppltn_rate_40": 18.9,
                "ppltn_rate_50": 11.7,
                "ppltn_rate_60": 6.3,
                "ppltn_rate_70": 3.7,
            }

        """
        try:
            ppltn_data_extract: dict[str, float] = {
                key.lower(): float(value)
                for key, value in data.items()
                if "PPLTN_RATE_" in key
            }
            return AgeCongestionSpecific(**ppltn_data_extract)
        except (ValidationError, ValueError) as error:
            logging.error("error --> %s", error)
            return None

    @classmethod
    def schema_modify(cls, data: dict[str, str]) -> "TotalAgeRateComposition":
        """
        인구 rate 스키마 정제

        Args:
            data (dict[str, str]): 서울시 인구 혼잡도 dictionary
                >>> a = {
                    "AREA_NM": "가로수길",
                    "AREA_CD": "POI059",
                    "AREA_CONGEST_LVL": "보통",
                    "AREA_CONGEST_MSG": "사람이 몰려있을 수 있지만 크게 붐비지는 않아요. 도보 이동에 큰 제약이 없어요.",
                    "AREA_PPLTN_MIN": "30000",
                    "AREA_PPLTN_MAX": "32000",
                    ...
                }

        Returns:
            >>> {
                "area_name": "가로수길",
                "area_congestion_lvl": "보통",
                "area_congestion_msg": "사람이 몰려있을 수 있지만 크게 붐비지는 않아요. 도보 이동에 큰 제약이 없어요.",
                "area_ppltn_min": 30000.0,
                "area_ppltn_max": 32000.0,
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
        ppltn_data_extract: dict[str, float] = cls._ppltn_data(data=data)
        return cls(
            area_name=data["AREA_NM"],
            area_congestion_lvl=data["AREA_CONGEST_LVL"],
            area_congestion_msg=data["AREA_CONGEST_MSG"],
            area_ppltn_min=int(data["AREA_PPLTN_MIN"]),
            area_ppltn_max=int(data["AREA_PPLTN_MAX"]),
            age_congestion_specific=ppltn_data_extract,
        )


class AreaGenderRateSpecific(BaseModel):
    """여성 남성 혼잡도"""

    male_ppltn_rate: float
    female_ppltn_rate: float


class GenderPopulationRate(TotalAgeRate):
    """여성 남성 혼잡도 비율"""

    gender_rate: AreaGenderRateSpecific

    @field_validator("gender_rate", mode="plain", check_fields=True)
    @classmethod
    def _ppltn_area(cls, data: dict[str, str]) -> AreaGenderRateSpecific:
        """
        인구 rate 추출

        Args:
            data (dict[str, str]): 서울시 인구 혼잡도 dictionary
                >>> a = {
                    "AREA_NM": "가로수길",
                    "AREA_CD": "POI059",
                    "AREA_CONGEST_LVL": "보통",
                    "AREA_CONGEST_MSG": "사람이 몰려있을 수 있지만 크게 붐비지는 않아요. 도보 이동에 큰 제약이 없어요.",
                    "AREA_PPLTN_MIN": "30000",
                    "AREA_PPLTN_MAX": "32000",
                    ...
                }
        Returns:
            >>> {'male_ppltn_rate': 44.2, 'female_ppltn_rate': 55.8}

        """
        ppltn_data_extract: dict[str, float] = {
            key.lower(): float(value)
            for key, value in data.items()
            if "E_PPLTN_RATE" in key
        }
        print(ppltn_data_extract)
        return AreaGenderRateSpecific(**ppltn_data_extract)

    @classmethod
    def schema_modify(cls, data: dict[str, str]) -> "TotalAgeRate":
        """
        인구 rate 스키마 정제

        Args:
            data (dict[str, str]): 서울시 인구 혼잡도 dictionary
                >>> a = {
                    "AREA_NM": "가로수길",
                    "AREA_CD": "POI059",
                    "AREA_CONGEST_LVL": "보통",
                    "AREA_CONGEST_MSG": "사람이 몰려있을 수 있지만 크게 붐비지는 않아요. 도보 이동에 큰 제약이 없어요.",
                    "AREA_PPLTN_MIN": "30000",
                    "AREA_PPLTN_MAX": "32000",
                    ...
                }

        Returns:
            >>> {
                "area_name": "가로수길",
                "area_congestion_lvl": "보통",
                "area_congestion_msg": "사람이 몰려있을 수 있지만 크게 붐비지는 않아요. 도보 이동에 큰 제약이 없어요.",
                "area_ppltn_min": 30000,
                "area_ppltn_max": 32000,
                "gender_rate": {"male_ppltn_rate": 44.2, "female_ppltn_rate": 55.8},
            }


        """
        ppltn_data_extract: dict[str, float] = cls._ppltn_area(data=data)
        return cls(
            area_name=data["AREA_NM"],
            area_congestion_lvl=data["AREA_CONGEST_LVL"],
            area_congestion_msg=data["AREA_CONGEST_MSG"],
            area_ppltn_min=int(data["AREA_PPLTN_MIN"]),
            area_ppltn_max=int(data["AREA_PPLTN_MAX"]),
            gender_rate=ppltn_data_extract,
        )
