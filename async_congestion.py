"""
async congestion
"""

import asyncio
import tracemalloc

from aiokafka.errors import KafkaConnectionError

from core.setting.create_log import SocketLogCustomer
from core.congestion.utils import seoul_place
from core.congestion.seoul_congestion_api import congestion
from core.data_mq.data_interaction import produce_sending
from core.data_mq.topic_create import create_topic

tracemalloc.start()

logging = SocketLogCustomer()


"""
비동기 5개 사용해야할듯 
"""


async def async_popular_congestion():
    """
    인구 혼잡도 kafka 연결
    """
    create_topic()
    while True:
        await asyncio.sleep(5)
        try:
            for category, location in seoul_place().items():
                for data in location:
                    congest = await congestion(data)
                    await produce_sending(topic=category, message=congest, key=category)
                    await logging.data_log(location=category, message=congest)
        except KafkaConnectionError as error:
            await logging.error_log(error_type="NotConnection", message=error)


asyncio.run(async_popular_congestion())
