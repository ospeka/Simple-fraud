from datetime import datetime
from pprint import pprint

import fastapi
import redis
import uvicorn

import models
import velocity_check

app = fastapi.FastAPI()
redis_obj = redis.Redis(host="localhost", port=6379, decode_responses=True)


@app.get("/")
def get():
    return {"message": "Hello, World!"}


@app.post("/check_transaction")
def check_transaction(transaction: models.Transaction):
    transaction.global_human_time = datetime.fromtimestamp(
        transaction.timestamp
    ).strftime("%Y-%m-%d %H:%M:%S")
    pprint(transaction)
    velocity_result = velocity_check.check_velocity(
        transaction.user_id, transaction.timestamp, transaction.id, redis_obj
    )
    return {
        "status": "Transaction checked successfully!",
        "velocity_result": velocity_result,
    }


@app.put("/change_rule")
def change_rule(rule_name: str, new_value: str):
    pprint(rule_name + " " + new_value)
    return {"status": "Rule changed successfully!"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
