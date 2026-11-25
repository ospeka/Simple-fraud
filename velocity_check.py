import time
import redis

WINDOW_SECONDS = 300  # 5 minutes
LIMIT_TRANSACTIONS = 5


def check_velocity(
    user_id: str, timestamp: int, transaction_id: int, redis_obj: redis.Redis
) -> dict[str, str]:
    print(f"Checking velocity for user {user_id} at timestamp {timestamp}")
    key = f"velocity:{user_id}"
    redis_obj.zadd(key, {str(transaction_id): timestamp})
    redis_obj.zremrangebyscore(
        key, 0, time.time() - WINDOW_SECONDS
    )  # Remove transactions older than 5 min
    transaction_count = redis_obj.zcard(key)

    if transaction_count > LIMIT_TRANSACTIONS:  # type: ignore
        print(f"User {user_id} has exceeded the transaction limit!")
        return {"status": "Transaction flagged for review!"}
    return {"status": "Transaction is within velocity limits."}
