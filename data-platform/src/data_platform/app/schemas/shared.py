from pydantic import BaseModel
from enum import StrEnum


class Traders(StrEnum):
    SUBMISSION = "SUBMISSION"


class Product(StrEnum):
    EMERALDS = "EMERALDS"
    TOMATOES = "TOMATOES"
    ASH_COATED_OSMIUM = "ASH_COATED_OSMIUM"
    INTARIAN_PEPPER_ROOT = "INTARIAN_PEPPER_ROOT"
    HYDROGEL_PACK = "HYDROGEL_PACK"
    VELVETFRUIT_EXTRACT = "VELVETFRUIT_EXTRACT"
    VEV_4000 = "VEV_4000"
    VEV_4500 = "VEV_4500"
    VEV_5000 = "VEV_5000"
    VEV_5100 = "VEV_5100"
    VEV_5200 = "VEV_5200"
    VEV_5300 = "VEV_5300"
    VEV_5400 = "VEV_5400"
    VEV_5500 = "VEV_5500"
    VEV_6000 = "VEV_6000"
    VEV_6500 ="VEV_6500"

class Filters(BaseModel):
    timestamp_min: int | None = None
    timestamp_max: int | None = None
