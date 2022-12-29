from sqlalchemy.orm import Session
from model.ants import Ant


def get_ant_by_id(ant_id: int, db:Session) -> Ant:
    query = db.query(Ant).get(ant_id)
    return query
