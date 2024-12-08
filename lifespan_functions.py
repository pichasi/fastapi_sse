"""_summary
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from dependencies import close_redis, initialize_redis


@asynccontextmanager
async def lifespan(application: FastAPI):
    """Shutdown event handler."""
    await initialize_redis()
    yield
    await close_redis()
