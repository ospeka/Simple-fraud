import time
from dataclasses import dataclass

import redis.asyncio as redis


@dataclass(frozen=True)
class VelocityResult:
    count: int
    exceeded: bool


async def check_velocity(
    redis_client: redis.Redis,
    user_id: str,
    transaction_id: str,
    *,
    window_seconds: int,
    limit: int,
    now: float | None = None,
) -> VelocityResult:
    """Count the user's transactions in a sliding window (Redis sorted set).

    - Time is the server's, never the client's.
    - All four commands run in one MULTI/EXEC, so concurrent checks of the
      same user cannot interleave between cleanup, add and count.
    - EXPIRE removes keys of inactive users.
    - The member is the transaction_id and zadd uses nx=True, so a client
      retry of the same transaction is not counted twice.
    - The current transaction is counted; exceeded means count > limit.
    """
    now = time.time() if now is None else now
    key = f"velocity:{user_id}"
    async with redis_client.pipeline(transaction=True) as pipe:
        pipe.zremrangebyscore(key, 0, now - window_seconds)
        pipe.zadd(key, {transaction_id: now}, nx=True)
        pipe.zcard(key)
        pipe.expire(key, window_seconds)
        _, _, count, _ = await pipe.execute()
    return VelocityResult(count=count, exceeded=count > limit)
