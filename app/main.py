from contextlib import asynccontextmanager
from typing import Annotated

import redis.asyncio as redis
from fastapi import Depends, FastAPI, Request

from app.config import Settings, get_settings
from app.engine import evaluate
from app.models import TransactionRequest, TransactionResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = redis.from_url(get_settings().redis_url, decode_responses=True)
    app.state.redis = client
    yield
    await client.aclose()


app = FastAPI(title="Simple Fraud", lifespan=lifespan)


def get_redis(request: Request) -> redis.Redis:
    return request.app.state.redis


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/transactions", response_model=TransactionResponse)
async def create_transaction(
    tx: TransactionRequest,
    redis_client: Annotated[redis.Redis, Depends(get_redis)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> TransactionResponse:
    return await evaluate(tx, redis_client, settings)
