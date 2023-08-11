"""
필요한 데이터스키마 나누기
"""
import logging
from pydantic import BaseModel
from pydantic_core import ValidationError


class TotalAgeRate(BaseModel):
    """나이 연령별 묶음"""

    area_name: str
    area_congestion_lvl: str
    area_congestion_msg: str
    area_ppltn_min: float
    area_ppltn_max: float


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

    age_congestion_specfic: AgeCongestionSpecific

    @classmethod
    def _modify_arch_table(cls, ppltn_data: dict[str, float]) -> AgeCongestionSpecific:
        try:
            return AgeCongestionSpecific(**ppltn_data)
        except ValidationError as error:
            logging.error("Error --> %s", error)

    @classmethod
    def schema_modify(
        cls,
        area_name: str,
        area_congestion_lvl: str,
        area_congestion_msg: str,
        area_ppltn_min: float,
        area_ppltn_max: float,
        ppltn_data: dict[str, float],
    ) -> "TotalAgeRateComposition":
        ppltn_data = {
            key: float(value)
            for key, value in ppltn_data.items()
            if "PPLTN_RATE_" in key
        }
        congestion_rate = cls._modify_arch_table(ppltn_data=ppltn_data)
        return cls(
            area_name=area_name,
            area_congestion_lvl=area_congestion_lvl,
            area_congestion_msg=area_congestion_msg,
            area_ppltn_min=area_ppltn_min,
            area_ppltn_max=area_ppltn_max,
            age_congestion_specfic=congestion_rate,
        )


class AreaSexCongestionSpecific(BaseModel):
    """여성 남성 혼잡도"""

    male_ppltn_rate: float
    female_ppltn_rate: float
