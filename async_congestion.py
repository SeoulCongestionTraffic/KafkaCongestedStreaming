"""
TEST
"""

if __name__ == "__main__":
    import asyncio
    from core.data_mq.topic_create import create_topic
    from core.data_mq.s3_sink_connect import (
        topic_gender,
        topic_age,
        topic_no_age,
        topic_no_gender,
        avg_topic_age,
        avg_topic_gender,
        avg_topic_n_age,
        avg_topic_n_gender,
    )
    from core.congestion_response.seoul_congestion_api import (
        AsyncSeoulCongestionDataSending as ADS,
    )
    from core.congestion_response.seoul_congestion_api import (
        AgeCongestionRate,
        GenderCongestionRate,
    )

    async def main():
        try:
            await create_topic()
            topic_gender
            topic_age
            topic_no_age
            topic_no_gender
            avg_topic_age
            avg_topic_gender
            avg_topic_n_age
            avg_topic_n_gender

            await asyncio.sleep(6)
            task = [
                asyncio.create_task(
                    ADS(AgeCongestionRate()).async_popular_congestion("AGE")
                ),
                asyncio.create_task(
                    ADS(GenderCongestionRate()).async_popular_congestion("GENDER")
                ),
            ]

            await asyncio.gather(*task)
        except Exception as error:
            print(error)

    # asyncio를 이용해 메인 함수를 실행
    asyncio.run(main())
