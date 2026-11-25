import requests
import random
import time


def random_transaction():
    trans = {
        "user_id": random.choice(["Hanna", "Josh", "Alex", "Emily"]),
        "id": random.randint(1, 1000),
        "amount": round(random.uniform(10.0, 1000.0), 2),
        "currency": random.choice(["USD", "EUR", "HRN"]),
        "timestamp": random.randint(int(time.time() - 300), int(time.time())),
        "location": random.choice(["New York", "London", "Kyiv"]),
    }
    return trans


for _ in range(6):
    resp = requests.post(
        "http://127.0.0.1:8000/check_transaction",
        json={**random_transaction(), "user_id": "Hanna"},
    )
    print(resp.json())

# resp = requests.put(
#     "http://127.0.0.1:8000/change_rule",
#     params={"rule_name": "max_amount", "new_value": "500.0"},
# )
# response = resp.json()
# print(response)
# print(response["status"])
