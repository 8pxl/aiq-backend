from __future__ import annotations
from sqlmodel import Field, SQLModel
from enum import Enum

class Qualification(Enum):
    NONE = 0
    REGIONAL = 1
    WORLD = 2

    @classmethod
    def from_string(cls, s: str) -> Qualification:
        mapping = {
            "Event Region Championship": cls.REGIONAL,
            "World Championship": cls.WORLD
        }
        return mapping.get(s, cls.NONE)

class Teams(SQLModel, table=True):
    id: int = Field(primary_key=True)
    number: str
    organization: str
    country: str
    region: str
    registered: bool
    grade: str
    qualification: Qualification
    world_rank: int
    score: int
    programming: int
    driver: int
