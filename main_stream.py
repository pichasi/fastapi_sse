from fastapi import Depends, FastAPI

from stream import EventStream
from sse_starlette.sse import EventSourceResponse
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "*",
]


app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=origins)



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
