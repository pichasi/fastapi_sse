"""_summary_
    """

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from custom_types import Order
from dependencies import RedisProvider, get_cache
from lifespan_functions import lifespan

origins = [
    "*",
]


app = FastAPI(lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=origins)


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


