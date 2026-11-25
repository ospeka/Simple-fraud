"""Send random transactions of one user to a running service."""
import random
import uuid

import httpx

URL = "http://127.0.0.1:8000/v1/transactions"


def random_transaction(user_id: str) -> dict:
    return {
        "transaction_id": str(uuid.uuid4()),
        "user_id": user_id,
        "amount": str(round(random.uniform(10.0, 1000.0), 2)),
        "currency": random.choice(["USD", "EUR", "UAH"]),
        "geo_location": random.choice(["US", "GB", "UA"]),
    }


if __name__ == "__main__":
    for _ in range(7):
        resp = httpx.post(URL, json=random_transaction("hanna"))
        print(resp.json())
