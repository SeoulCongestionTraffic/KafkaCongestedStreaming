"""
추상화 집단
"""

from abc import ABC, abstractmethod


class AbstractResponseParser(ABC):
    """
    Abstract class for response parsers.
    """

    @abstractmethod
    async def xml_to_dict_convert(self, response: str) -> dict:
        """
        XML 문자열을 딕셔너리로 변환.

        Parameters:
        - xml_string (str): XML 형태의 문자열.

        Returns:
        - dict[str, Any]: XML을 딕셔너리로 변환한 결과.
        """
        raise NotImplementedError()
