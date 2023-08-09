import logging
from pathlib import Path


def log(name: str, log_location: str) -> logging.Logger:
    """
    주어진 이름으로 로거를 생성하거나 가져옵니다. 스트림 및 파일 핸들러가 존재하지 않는 경우 로거에 추가합니다.

    매개변수:
    - name: 로거의 이름.
    - log_location: 로그 파일을 저장할 경로.

    반환값:
    - 로거 객체.
    """
    logger = logging.getLogger(name=name)
    if logger.hasHandlers():
        return logger

    logger.propagate = False
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    try:
        file_handler = logging.FileHandler(filename=log_location)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except (FileNotFoundError, FileExistsError) as error:
        logger.error("Failed to create file handler due to: %s", error)
        # 파일이 없을 때 파일을 생성하도록 수정
        Path(log_location).parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(filename=log_location)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


class SocketLogCustomer:
    """
    Log 생성 정형화
    """

    def __init__(self, base_path: Path = None):
        """
        기본 또는 지정된 base_path로 SocketLogCustomer를 초기화합니다.

        매개변수:
        - base_path: 로그 파일이 저장될 경로.
        """
        if base_path:
            self.base_path = base_path
        else:
            self.base_path = Path(__file__).parent.parent.parent / "streaming" / "log"

    def create_logger(self, log_name: str, log_type: str) -> logging.Logger:
        """
        지정된 로그 이름과 유형을 사용하여 로거를 생성합니다.

        매개변수:
        - log_name: 로그 파일의 이름.
        - log_type: 로그의 유형 (connection, data 등).

        반환값:
        - 로거 객체.
        """
        try:
            log_path = self.base_path / log_type / log_name
            log_path.parent.mkdir(parents=True, exist_ok=True)
            return log(log_name.split(".")[0], str(log_path))
        except (FileNotFoundError, FileExistsError) as error:
            logger = logging.getLogger(__name__)
            logger.error("Failed to create or access the log file: %s", error)
            return logger

    async def log_message(
        self, log_name: str, log_type: str, message: str, level: str = "info"
    ):
        """
        지정된 로그 이름, 유형 및 레벨을 사용하여 메시지를 기록합니다.

        매개변수:
        - log_name: 로그 파일의 이름.
        - log_type: 로그의 유형 (connection, data 등).
        - message: 기록될 메시지.
        - level: 로깅 레벨 (기본값은 "info").
        """
        logger = self.create_logger(log_name, log_type)
        log_func = getattr(logger, level, "info")
        log_func(message)

    async def connection(self, location: str, message: str):
        """
        특정 거래소와 관련된 연결 메시지를 기록합니다.

        매개변수:
        - location: 장소의 이름.
        - message: 기록될 메시지.
        """
        log_name = f"{location}_connection.log"
        await self.log_message(log_name, "connection", message)

    async def data_log(self, location: str, message: str):
        log_name = f"{location}_data.log"
        await self.log_message(log_name, "data", message)

    async def error_log(self, error_type: str, message: str):
        log_name = f"{error_type}.log"
        await self.log_message(log_name, "error", message, level="error")
