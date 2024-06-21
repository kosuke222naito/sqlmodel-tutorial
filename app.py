from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select


class HeroTeamLink(SQLModel, table=True):
    team_id: int | None = Field(default=None, foreign_key="team.id", primary_key=True)
    hero_id: int | None = Field(default=None, foreign_key="hero.id", primary_key=True)


class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str

    heroes: list["Hero"] = Relationship(back_populates="teams", link_model=HeroTeamLink)


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)

    teams: list[Team] = Relationship(back_populates="heroes", link_model=HeroTeamLink)


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=False)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_heroes():
    with Session(engine) as session:
        team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
        team_z_force = Team(name="Z-Force", headquarters="Sister Margaret's Bar")

        hero_deadpond = Hero(
            name="Deadpond",
            secret_name="Dive Wilson",
            teams=[team_z_force, team_preventers],
        )
        hero_rusty_man = Hero(
            name="Rusty-Man", secret_name="Tommy Sharp", age=48, teams=[team_preventers]
        )
        hero_spider_boy = Hero(
            name="Spider-Boy", secret_name="Pedro Parqueador", teams=[team_preventers]
        )
        session.add(hero_deadpond)
        session.add(hero_rusty_man)
        session.add(hero_spider_boy)
        session.commit()

        session.refresh(hero_deadpond)
        session.refresh(hero_rusty_man)
        session.refresh(hero_spider_boy)

        print(f"Deadpond: {hero_deadpond}")
        print(f"Deadpond teams: {hero_deadpond.teams}")
        print(f"Rusty-Man: {hero_rusty_man}")
        print(f"Rusty-Man teams: {hero_rusty_man.teams}")
        print(f"Spider-Boy: {hero_spider_boy}")
        print(f"Spider-Boy teams: {hero_spider_boy.teams}")


def select_heroes():
    with Session(engine) as session:
        statement = select(Team).where(Team.name == "Preventers")
        result = session.exec(statement)
        team_preventers = result.one()

        print("Preventers heroes:", team_preventers.heroes)


def update_heroes():
    with Session(engine) as session:
        hero_spider_boy = session.exec(
            select(Hero).where(Hero.name == "Spider-Boy")
        ).one()

        preventers_team = session.exec(
            select(Team).where(Team.name == "Preventers")
        ).one()

        print("Hero Spider-Boy:", hero_spider_boy)
        print("Preventers Team:", preventers_team)
        print("Preventers Team Heroes:", preventers_team.heroes)

        hero_spider_boy.team = None

        print("Spider-Boy without team:", hero_spider_boy)

        print("Preventers Team Heroes again:", preventers_team.heroes)

        session.add(hero_spider_boy)
        session.commit()
        print("After committing")

        session.refresh(hero_spider_boy)
        print("Spider-Boy after commit:", hero_spider_boy)

        print("Preventers Team Heroes after commit:", preventers_team.heroes)


def main():
    create_db_and_tables()
    create_heroes()
    # select_heroes()
    # update_heroes()


if __name__ == "__main__":
    main()
