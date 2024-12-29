from typing import Iterable, List

from cassandra.cluster import Session

import models as m
from const import KEY_SPACE
from db.utils import convert_lists


def create_teacher(session: Session, user_id: str):
    session.execute(
        f"""
        INSERT INTO {KEY_SPACE}.teacher 
            (user_id  , students)
        VALUES 
            ({user_id}, []);
        """
    )


def get_all_teachers(session: Session) -> Iterable[m.Teacher]:
    teachers_db = session.execute(
        f"""
        SELECT *
        FROM {KEY_SPACE}.teacher;
        """
    )
    teachers = []
    for t in teachers_db:
        kwarg = {k: convert_lists(t, k) for k in teachers_db.column_names}
        kwarg["user_id"] = str(kwarg["user_id"])
        teachers.append(m.Teacher(**kwarg))
    return teachers


def get_teacher(session: Session, user_id: str) -> m.Teacher:
    ressult_db = session.execute(
        f"""
        SELECT *
        FROM {KEY_SPACE}.teacher;
        """
    )
    first_result = ressult_db.one()
    kwarg = {k: convert_lists(first_result, k) for k in ressult_db.column_names}
    kwarg["user_id"] = str(kwarg["user_id"])
    return m.Teacher(**kwarg)


def assign_students(session: Session, user_id: str, students: List[str]):
    session.execute(
        f"""
        UPDATE {KEY_SPACE}.teacher
        SET students={str(students).replace("'","")}
        WHERE user_id={user_id};
        """
    )
