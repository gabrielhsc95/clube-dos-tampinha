from typing import Iterable, List

from cassandra.cluster import Session

import models as m
from const import KEY_SPACE
from db.utils import convert_lists


def create_student(session: Session, user_id: str, parents: List[str]):
    session.execute(
        f"""
        INSERT INTO {KEY_SPACE}.student 
            (user_id  , parents                        , activities)
        VALUES 
            ({user_id}, {str(parents).replace("'", "")}, []);
        """
    )


def get_all_students(session: Session) -> Iterable[m.Student]:
    students_db = session.execute(
        f"""
        SELECT *
        FROM {KEY_SPACE}.student;
        """
    )
    students = []
    for s in students_db:
        kwarg = {k: convert_lists(s, k) for k in students_db.column_names}
        kwarg["user_id"] = str(kwarg["user_id"])
        students.append(m.Student(**kwarg))
    return students


def get_student(session: Session, user_id: str) -> m.Student:
    results_db = session.execute(
        f"""
        SELECT *
        FROM {KEY_SPACE}.student
        WHERE user_id={user_id};
        """
    )
    first_result = results_db.one()
    kwarg = {k: convert_lists(first_result, k) for k in results_db.column_names}
    kwarg["user_id"] = str(kwarg["user_id"])
    return m.Student(**kwarg)
