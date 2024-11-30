from faststream.rabbit import RabbitBroker
from config.settings import settings

broker = RabbitBroker(url=settings.rabbit_url)


async def publish_bitcoin_rate(rate: str):
    async with broker as br:
        await br.publish(rate, "tasks")
