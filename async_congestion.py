"""
async congestion
"""

import tracemalloc
import asyncio

from core.congestion.utils import place_unique
from core.congestion.seoul_congestion_api import congestion
from core.data_mq.data_interaction import produce_sending
from core.data_mq.topic_create import create_topic


tracemalloc.start()


async def async_popular_congestion():
    """
    인구 혼잡도 kafka 연결
    """
    create_topic()
    await asyncio.sleep(1)

    try:
        for category, location in place_unique().items():
            for data in location:
                t = await congestion(data)
                await produce_sending(topic=category, message=t, key=category)
    except (TypeError, ValueError) as error:
        print(error)


asyncio.run(async_popular_congestion())
