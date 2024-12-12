from datetime import date
from typing import Iterable

from cassandra.cluster import Session

import models as m
from const import KEY_SPACE


def create_activity(
    session: Session,
    teacher_id: str,
    date: date,
    student_id: str,
    grade: float,
    title: str,
    report: str,
):
    session.execute(
        f"""
        INSERT INTO {KEY_SPACE}.activity 
            (id    , responsible_teacher, date                                 , student     , grade  , title  , report)
        VALUES 
            (uuid(), {teacher_id}       , toDate('{date.strftime("%Y-%m-%d")}'), {student_id}, {grade}, {title}, {report});
        """
    )


def get_activities(session: Session, student_id: str) -> Iterable[m.Activity]:
    activities_db = session.execute(
        f"""
        SELECT *
        FROM {KEY_SPACE}.activity
        WHERE student_id={student_id}
        ALLOW FILTERING;
        """
    )
    activities = []
    for a in activities_db:
        kwarg = {k: getattr(a, k) for k in activities.column_names}
        activities.append(m.Activity(**kwarg))
    return activities
