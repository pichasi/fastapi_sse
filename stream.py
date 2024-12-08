"""_summary_
    """

import asyncio
from fastapi import Depends
from dependencies import get_cache, RedisProvider


class EventStream:
    """_summary_"""

    def __init__(self, cache: RedisProvider = Depends(get_cache)):

        self.cache = cache

    async def execute(self, channel: str):
        """_summary_

        Args:
            channel (str): _description_

        Yields:
            _type_: _description_
        """

        sub = self.cache.pubsub()

        if sub:
            await sub.subscribe(channel)

            try:
                while True:
                    async for event in sub.listen():
                        if event:
                            if isinstance(event, dict):
                                event_type = event.get("type", None)
                                match (event_type):
                                    case "subscribe":
                                        event = {
                                            "event": "subscribe",
                                            "data": {"some_data": "some_value"},
                                        }
                                    case "message":
                                        print(f"Got message {event}")
                                        event = {
                                            "event": "message",
                                            "data": event["data"],
                                        }
                                    case _:
                                        print(f"Unknown event type. {event}")
                                        event = {"event": "Unknown", "data": 1}
                            yield event
                    # await asyncio.sleep(1)
            except Exception as e:
                print(f"Some exception: {str(e)}")
            except asyncio.CancelledError:
                print(f"Disconnecting from channel {channel}")
                await sub.unsubscribe(f"{channel}")

    def get_event_data(self, event):
        """_summary_

        Args:
            event (_type_): _description_

        Returns:
            _type_: _description_
        """

        event_to_return = {}

        data = event.get("data", None)
        if not data:
            return event

        event_to_return["event"] = "message"
        event_to_return["data"] = data

        return event_to_return
