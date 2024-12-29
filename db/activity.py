from datetime import date, datetime
from typing import Iterable

from cassandra.cluster import Session

import models as m
from const import KEY_SPACE


def create_activity(
    session: Session,
    teacher_id: str,
    date_: date,
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
            (uuid(), {teacher_id}       , toDate('{date_.strftime("%Y-%m-%d")}'), {student_id}, {grade}, '{title}', '{report}');
        """
    )


def get_activities(
    session: Session, student_id: str, responsible_teacher: str
) -> Iterable[m.Activity]:
    activities_db = session.execute(
        f"""
        SELECT *
        FROM {KEY_SPACE}.activity
        WHERE student={student_id}
          AND responsible_teacher={responsible_teacher}
        ALLOW FILTERING;
        """
    )
    activities = []
    for a in activities_db:
        kwarg = {k: getattr(a, k) for k in activities_db.column_names}
        kwarg["id"] = str(kwarg["id"])
        kwarg["responsible_teacher"] = str(kwarg["responsible_teacher"])
        kwarg["student"] = str(kwarg["student"])
        kwarg["date"] = datetime.strptime(str(kwarg["date"]), "%Y-%m-%d").date()
        activities.append(m.Activity(**kwarg))
    return activities
