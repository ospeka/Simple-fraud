import redis.asyncio as redis

from app.config import Settings
from app.models import Decision, TransactionRequest, TransactionResponse
from app.velocity import check_velocity


async def evaluate(
    tx: TransactionRequest, redis_client: redis.Redis, settings: Settings
) -> TransactionResponse:
    """Run the rule pipeline. Stage 1: velocity check only."""
    reasons: list[str] = []

    velocity = await check_velocity(
        redis_client,
        tx.user_id,
        tx.transaction_id,
        window_seconds=settings.velocity_window_seconds,
        limit=settings.velocity_limit,
    )
    if velocity.exceeded:
        reasons.append(
            f"velocity: {velocity.count} transactions in "
            f"{settings.velocity_window_seconds}s (limit {settings.velocity_limit})"
        )

    decision = Decision.DECLINE if reasons else Decision.APPROVE
    return TransactionResponse(
        transaction_id=tx.transaction_id, decision=decision, reasons=reasons
    )
