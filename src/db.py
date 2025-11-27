from datetime import datetime
from typing import Any
from sqlalchemy import Engine
from sqlmodel import Session, select
from tables import Qualification, Teams, Metadata

def get_all_teams(engine: Engine) -> list[int]:
    ids = []
    with Session(engine) as session:
        return list(session.exec(select(Teams.id)).all())

def upsert(engine: Engine, x: Any):
    with Session(engine) as session:
        _ = session.merge(x)
        session.commit()

def qualify(engine: Engine, id: int):
    with Session(engine) as session:
        existing = session.get(Teams,id)
        if not existing:
            print(f"team {id} doesnt exist yet!")
            return
        else:
            existing.qualification = Qualification.WORLD
        session.commit();
def set_update_time(engine: Engine):
    with Session(engine) as session:
        session.get(Metadata)

def get_last_qualification_update(engine: Engine)-> datetime: 
    with Session(engine) as session:
        return(session.exec(select(Metadata.last_updated_qualifications)).one())

    # existing = session.get(Teams, team.id)
    #     if not existing:
    #         session.add(team)
    #     else:
    #         existing.score = team.score
    #         existing.driver = team.driver
    #         existing.rank = team.world_rank
    #         existing.programming = team.programming
    #         existing.qualification = team.qualification
    #     session.commit()
