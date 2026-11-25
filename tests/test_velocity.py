import fakeredis.aioredis
import pytest

from app.velocity import check_velocity

WINDOW = 300
LIMIT = 5


@pytest.fixture
async def r():
    client = fakeredis.aioredis.FakeRedis(decode_responses=True)
    yield client
    await client.aclose()


async def check(r, user, tx_id, now):
    return await check_velocity(
        r, user, tx_id, window_seconds=WINDOW, limit=LIMIT, now=now
    )


async def test_within_limit(r):
    for i in range(LIMIT):
        result = await check(r, "u1", f"t{i}", now=1000 + i)
    assert result.count == LIMIT
    assert not result.exceeded


async def test_exceeds_on_next_transaction(r):
    for i in range(LIMIT):
        await check(r, "u1", f"t{i}", now=1000 + i)
    result = await check(r, "u1", "t_over", now=1010)
    assert result.count == LIMIT + 1
    assert result.exceeded


async def test_old_transactions_leave_window(r):
    for i in range(LIMIT):
        await check(r, "u1", f"t{i}", now=1000 + i)
    result = await check(r, "u1", "t_late", now=1000 + WINDOW + 100)
    assert result.count == 1
    assert not result.exceeded


async def test_retry_of_same_transaction_not_counted_twice(r):
    await check(r, "u1", "t1", now=1000)
    result = await check(r, "u1", "t1", now=1001)
    assert result.count == 1


async def test_users_are_isolated(r):
    for i in range(LIMIT + 1):
        await check(r, "u1", f"t{i}", now=1000 + i)
    result = await check(r, "u2", "t0", now=1010)
    assert result.count == 1


async def test_key_has_ttl(r):
    await check(r, "u1", "t1", now=1000)
    ttl = await r.ttl("velocity:u1")
    assert 0 < ttl <= WINDOW
