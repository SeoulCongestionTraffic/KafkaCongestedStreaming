"""
필요한 데이터스키마 나누기
"""
from pydantic import BaseModel
from pydantic_core import ValidationError


class AreaSexCongestionSpecific(BaseModel):
    """여성 남성 혼잡도"""

    male_ppltn_rate: float
    female_ppltn_rate: float


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


class TotalAgeRate(BaseModel):
    """나이 연령별 묶음"""

    area_name: str
    area_congestion_lvl: str
    area_congestion_msg: str
    area_ppltn_min: float
    area_ppltn_max: float
    age_congestion_specfic: dict[str, float] = AgeCongestionSpecific

    @classmethod
    def _modify_arch_table(cls, ppltn_data: dict[str, float]) -> AgeCongestionSpecific:
        """스키마 제설계"""
        try:
            return AgeCongestionSpecific(
                ppltn_rate_0=float(ppltn_data["PPLTN_RATE_0"]),
                ppltn_rate_10=float(ppltn_data["PPLTN_RATE_10"]),
                ppltn_rate_20=float(ppltn_data["PPLTN_RATE_20"]),
                ppltn_rate_30=float(ppltn_data["PPLTN_RATE_30"]),
                ppltn_rate_40=float(ppltn_data["PPLTN_RATE_40"]),
                ppltn_rate_50=float(ppltn_data["PPLTN_RATE_50"]),
                ppltn_rate_60=float(ppltn_data["PPLTN_RATE_60"]),
                ppltn_rate_70=float(ppltn_data["PPLTN_RATE_70"]),
            )
        except ValidationError as error:
            # 임시로 Exception 세부 에러는 pydantic error를 확인해서 커스텀 해야함
            print("Error --> %s", error)

    @classmethod
    def schema_modify(cls) -> AgeCongestionSpecific:
        """스키만 적용하는곳"""
        pass
