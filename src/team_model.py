from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Relationship, Field

if TYPE_CHECKING:
    from .hero_model import Hero


class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(default=None, index=True)
    headquarters: str

    heroes: list["Hero"] = Relationship(back_populates="team")
