from typing import Any, Iterable, List

from cassandra.cluster import Session

import models as m
from const import KEY_SPACE
from db.utils import convert_none_to_empty_list


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
        kwarg = {k: convert_none_to_empty_list(p, k) for k in parents_db.column_names}
        kwarg["user_id"] = str(kwarg["user_id"])
        print(kwarg)
        parents.append(m.Parent(**kwarg))
    return parents
