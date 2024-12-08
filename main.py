"""_summary_
    """

from fastapi import Depends, FastAPI
from sse_starlette.sse import EventSourceResponse

from custom_types import Order
from dependencies import RedisProvider, get_cache
from stream import EventStream
from lifespan_functions import lifespan


app = FastAPI(lifespan=lifespan)


# 1. Basic Setup
@app.get("/order/update")
async def order_update(order: Order, cache: RedisProvider = Depends(get_cache)):
    """_summary_

    Args:
        order (Order): _description_
        cache (RedisProvider, optional): _description_. Defaults to Depends(get_cache).

    Returns:
        _type_: _description_
    """

    await cache.publish(
        order.channel, {"order": order.order_id, "status": order.status}
    )
    return {"order": order.order_id, "status": order.status}


@app.get("/subscribe/{channel}")
async def stream_events(channel: str, stream: EventStream = Depends()):
    """_summary_

    Args:
        channel (str): _description_
        stream (EventStream, optional): _description_. Defaults to Depends().

    Returns:
        _type_: _description_
    """

    return EventSourceResponse(stream.execute(channel))
