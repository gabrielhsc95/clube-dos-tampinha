from typing import Iterable

from cassandra.cluster import Session

import models as m
from const import KEY_SPACE
from db.utils import convert_lists


def create_parent(session: Session, user_id: str):
    session.execute(
        f"""
        INSERT INTO {KEY_SPACE}.parent 
                (user_id  , children, payments)
        VALUES 
            ({user_id}, []      , []);
        """
    )


def get_all_parents(session: Session) -> Iterable[m.Parent]:
    parents_db = session.execute(
        f"""
        SELECT *
        FROM {KEY_SPACE}.parent;
        """
    )
    parents = []
    for p in parents_db:
        kwarg = {k: convert_lists(p, k) for k in parents_db.column_names}
        kwarg["user_id"] = str(kwarg["user_id"])
        parents.append(m.Parent(**kwarg))
    return parents


def get_parent(session: Session, user_id: str) -> m.Parent:
    result_db = session.execute(
        f"""
        SELECT *
        FROM {KEY_SPACE}.parent
        WHERE user_id={user_id};
        """
    )
    first_result = result_db.one()
    kwarg = {k: convert_lists(first_result, k) for k in result_db.column_names}
    kwarg["user_id"] = str(kwarg["user_id"])
    return m.Parent(**kwarg)
