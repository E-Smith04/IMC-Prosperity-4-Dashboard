from pydantic import BaseModel
from enum import StrEnum


class Traders(StrEnum):
    SUBMISSION = "SUBMISSION"


class Product(StrEnum):
    EMERALDS = "EMERALDS"
    TOMATOES = "TOMATOES"


class Filters(BaseModel):
    timestamp_min: int | None = None
    timestamp_max: int | None = None
