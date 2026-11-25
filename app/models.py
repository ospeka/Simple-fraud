from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, Field


class Decision(StrEnum):
    APPROVE = "APPROVE"
    DECLINE = "DECLINE"
    REVIEW = "REVIEW"


class TransactionRequest(BaseModel):
    transaction_id: str = Field(min_length=1, max_length=64)
    user_id: str = Field(min_length=1, max_length=64)
    amount: Decimal = Field(gt=0)
    currency: str = Field(pattern=r"^[A-Z]{3}$")
    ip_address: str | None = None
    geo_location: str | None = None


class TransactionResponse(BaseModel):
    transaction_id: str
    decision: Decision
    reasons: list[str] = []
