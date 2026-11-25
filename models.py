import pydantic


class User(pydantic.BaseModel):
    id: int
    full_name: str
    email: str
    base_country: str


class Transaction(pydantic.BaseModel):
    id: int
    user_id: str
    amount: float
    currency: str
    timestamp: int
    location: str
    user: User
    global_human_time: str | None = None
