# Simple Fraud: Anti-Fraud Transaction Monitoring Service

## 1. Overview
A microservice for real-time transaction monitoring. It ingests a transaction, runs it through a set of rules and returns a verdict.

## 2. Goals
* Scalable REST API for high-throughput transaction processing.
* **Velocity checks** on an in-memory store (Redis).
* Reliable persistence of transaction history and user profiles.
* An analytical layer for reporting suspicious activity.

## 3. Technology Stack
* **Language:** Python 3.12+ (asyncio)
* **Web framework:** FastAPI
* **In-memory store:** Redis (counters, rate limiting)
* **Primary database:** PostgreSQL (raw SQL via `asyncpg`)
* **Infrastructure:** Docker, Docker Compose
* **Testing:** Pytest

## 4. Quick Start
```bash
cp .env.example .env
docker compose up -d redis db
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```
Send test traffic: `python scripts/send_transactions.py`. Run tests: `pytest`.

## 5. API
`POST /v1/transactions`

```json
{
  "transaction_id": "7b0c...",
  "user_id": "hanna",
  "amount": "99.90",
  "currency": "USD",
  "ip_address": "203.0.113.5",
  "geo_location": "UA"
}
```
Response:
```json
{"transaction_id": "7b0c...", "decision": "APPROVE", "reasons": []}
```
`GET /health` is a liveness check.

## 6. Rule Engine
Every transaction goes through a pipeline of rules (`app/engine.py`):
1. **Velocity check** (implemented): more than `VELOCITY_LIMIT` transactions per user within `VELOCITY_WINDOW_SECONDS` leads to `DECLINE`.
2. **High-amount check** (planned): amount above a per-user threshold.
3. **Geo-mismatch** (planned): transaction country differs from the user's home country.

Decisions: `APPROVE`, `DECLINE`, `REVIEW` (manual inspection, used by upcoming rules).

## 7. Data Architecture
* **Redis (hot data):** `velocity:{user_id}` sorted set (member = `transaction_id`, score = server time). Cleanup, add, count and `EXPIRE` run in one `MULTI/EXEC`, so concurrent checks are atomic.
* **PostgreSQL (cold data, planned):** `users` (security profiles) and `transactions` (audit log), accessed with optimized raw SQL.

## 8. Non-Functional Requirements
* **Performance:** single transaction check under 100 ms.
* **Reliability:** data integrity via PostgreSQL ACID.
* **Scalability:** stateless service, horizontal scaling across containers.

## 9. Roadmap
- [x] Docker Compose for Redis and PostgreSQL
- [x] Redis-based velocity check (atomic, with TTL)
- [x] FastAPI endpoint and rule engine skeleton (velocity rule only)
- [x] First tests (velocity, API)
- [ ] Database schema via SQL scripts and `asyncpg` storage
- [ ] High-amount and geo-mismatch rules
- [ ] Idempotency key
- [ ] 80%+ test coverage

## License
MIT
