import fakeredis.aioredis
import httpx
import pytest

from app.main import app, get_redis


@pytest.fixture
async def client():
    fake = fakeredis.aioredis.FakeRedis(decode_responses=True)
    app.dependency_overrides[get_redis] = lambda: fake
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()
    await fake.aclose()


def payload(tx_id: str, **overrides) -> dict:
    data = {
        "transaction_id": tx_id,
        "user_id": "hanna",
        "amount": "99.90",
        "currency": "USD",
    }
    return {**data, **overrides}


async def test_health(client):
    resp = await client.get("/health")
    assert resp.status_code == 200


async def test_approve(client):
    resp = await client.post("/v1/transactions", json=payload("t1"))
    assert resp.status_code == 200
    body = resp.json()
    assert body["decision"] == "APPROVE"
    assert body["reasons"] == []


async def test_decline_after_velocity_limit(client):
    decisions = []
    for i in range(7):
        resp = await client.post("/v1/transactions", json=payload(f"t{i}"))
        decisions.append(resp.json()["decision"])
    assert decisions[:5] == ["APPROVE"] * 5
    assert decisions[5:] == ["DECLINE"] * 2


async def test_decline_has_reason(client):
    for i in range(6):
        resp = await client.post("/v1/transactions", json=payload(f"t{i}"))
    assert "velocity" in resp.json()["reasons"][0]


@pytest.mark.parametrize(
    "overrides",
    [{"amount": "0"}, {"amount": "-5"}, {"currency": "usd"}, {"currency": "USDD"}],
)
async def test_validation_errors(client, overrides):
    resp = await client.post("/v1/transactions", json=payload("t1", **overrides))
    assert resp.status_code == 422
