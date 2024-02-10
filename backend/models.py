import uuid
from typing import Optional
from pydantic import BaseModel, Field


class Fact(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    title: str = Field(...)
    author: str = Field(...)
    fact: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "title": "Monkeys",
                "author": "Admin",
                "fact": "If monkeys eat too many un-ripe bananas their tongue and eyes will turn green."
            }
        }


class FactUpdate(BaseModel):
    title: Optional[str]
    author: Optional[str]
    fact: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "title": "Monkeys",
                "author": "Admin",
                "fact": "If monkeys eat too many un-ripe bananas their tongue and eyes will turn green."
            }
        }
