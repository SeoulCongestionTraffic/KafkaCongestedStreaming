"""
TEST
"""

if __name__ == "__main__":
    import asyncio
    from core.congestion_response.seoul_congestion_api import (
        AsyncSeoulCongestionDataSending as ADS,
    )

    asyncio.run(ADS().async_popular_congestion())
