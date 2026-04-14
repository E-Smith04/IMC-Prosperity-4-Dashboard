from pydantic import BaseModel
from enum import StrEnum


class Traders(StrEnum):
    SUBMISSION = "SUBMISSION"


class Product(StrEnum):
    EMERALDS = "EMERALDS"
    TOMATOES = "TOMATOES"
    ASH_COATED_OSMIUM = "ASH_COATED_OSMIUM"
    INTARIAN_PEPPER_ROOT = "INTARIAN_PEPPER_ROOT"


class Filters(BaseModel):
    timestamp_min: int | None = None
    timestamp_max: int | None = None
