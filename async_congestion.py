"""
TEST
"""

if __name__ == "__main__":
    import asyncio
    from core.data_mq.s3_sink_connect import sink_connection
    from core.congestion_response.seoul_congestion_api import (
        AsyncSeoulCongestionDataSending as ADS,
    )
    from core.congestion_response.seoul_congestion_api import (
        AgeCongestionRate,
        GenderCongestionRate,
    )

    async def main():
        task = [
            asyncio.create_task(
                ADS(AgeCongestionRate()).async_popular_congestion("AGE")
            ),
            asyncio.create_task(
                ADS(GenderCongestionRate()).async_popular_congestion("GENDER")
            ),
            asyncio.create_task(sink_connection()),
        ]
        await asyncio.gather(*task)

    # asyncio를 이용해 메인 함수를 실행
    asyncio.run(main())
