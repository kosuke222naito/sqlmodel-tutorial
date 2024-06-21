from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Relationship, Field

if TYPE_CHECKING:
    from .team_model import Team


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)

    team_id: int | None = Field(default=None, foreign_key="team.id")
    team: "Team" = Relationship(back_populates="heroes")
