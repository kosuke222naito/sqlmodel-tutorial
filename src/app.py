from sqlmodel import Session

from .database import create_db_and_tables, engine
from .hero_model import Hero
from .team_model import Team


def create_heroes():
    with Session(engine) as session:
        team_z_force = Team(name="Z-Force", headquarters="Sister Margaret's Bar")

        hero_deadpond = Hero(
            name="Deadpond", secret_name="Dive Wilson", team=team_z_force
        )
        session.add(hero_deadpond)
        session.commit()

        session.refresh(hero_deadpond)

        print(f"Created Hero: {hero_deadpond}")
        print(f"Hero's team: {hero_deadpond.team}")

        hero_rusty_man = Hero(name="Rusty-Man", secret_name="secrete name")
        session.add(hero_rusty_man)
        session.commit()

        session.refresh(hero_rusty_man)
        print(f"Created Hero: {hero_rusty_man}")
        print(f"Hero's team: {hero_rusty_man.team}")


def main():
    create_db_and_tables()
    create_heroes()


if __name__ == "__main__":
    main()
