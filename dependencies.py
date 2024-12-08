"""_summary_

    Returns:
        _type_: _description_

    Yields:
        _type_: _description_
    """

import redis.asyncio as redis

redis_connection_pool = None


class RedisProvider:
    """_summary_"""

    def __init__(self):
        self.client = redis.Redis(connection_pool=redis_connection_pool)

    def pubsub(self):
        """_summary_

        Returns:
            _type_: _description_
        """

        return self.client.pubsub()

    async def publish(self, channel, message):
        """_summary_

        Args:
            channel (_type_): _description_
            message (_type_): _description_

        Returns:
            _type_: _description_
        """

        return await self.client.publish(channel, str(message))

    async def close(self):
        """_summary_"""

        await redis_connection_pool.disconnect()


async def initialize_redis():
    """Initialize redis."""

    print("Initializing redis..")

    global redis_connection_pool

    redis_connection_pool = redis.ConnectionPool.from_url(
        "redis://localhost:6379",
        decode_responses=True,
    )


async def close_redis():
    """Close the redis connection pool."""
    global redis_connection_pool

    print("Closing redis...")

    await redis_connection_pool.disconnect()


async def get_cache():
    """_summary_

    Yields:
        _type_: _description_
    """

    redis_provider = RedisProvider()

    yield redis_provider
