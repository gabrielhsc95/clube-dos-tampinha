from datetime import date, datetime
from typing import Iterable

from cassandra.cluster import Session

import models as m
from const import KEY_SPACE
from db.user import get_names


def create_invoice(
    session: Session,
    value: float,
    due_date: date,
    reason: str,
    student_id: str,
):
    session.execute(
        f"""
        INSERT INTO {KEY_SPACE}.payment 
            (id    , value  , due_date                                 , status                           , payment_date, paid_by, reason    , student)
        VALUES 
            (uuid(), {value}, toDate('{due_date.strftime("%Y-%m-%d")}'), '{m.PaymentStatus.Waiting.value}', null        , null   , '{reason}', {student_id});
        """
    )


def get_all_payments(session: Session) -> Iterable[m.Payment]:
    payments_db = session.execute(
        f"""
        SELECT *
        FROM {KEY_SPACE}.payment
        """
    )
    payments = []
    for p in payments_db:
        kwarg = {k: getattr(p, k) for k in payments_db.column_names}
        kwarg["id"] = str(kwarg["id"])
        kwarg["due_date"] = datetime.strptime(str(kwarg["due_date"]), "%Y-%m-%d").date()
        kwarg["student"] = str(kwarg["student"])
        if kwarg["paid_by"]:
            kwarg["paid_by"] = str(kwarg["paid_by"])
        payments.append(m.Payment(**kwarg))
    return payments


def get_all_payments_by_student(
    session: Session, student_id: str
) -> Iterable[m.Payment]:
    payments_db = session.execute(
        f"""
        SELECT *
        FROM {KEY_SPACE}.payment
        WHERE student={student_id}
        ALLOW FILTERING;
        """
    )
    payments = []
    for p in payments_db:
        kwarg = {k: getattr(p, k) for k in payments_db.column_names}
        kwarg["id"] = str(kwarg["id"])
        kwarg["due_date"] = datetime.strptime(str(kwarg["due_date"]), "%Y-%m-%d").date()
        kwarg["student"] = str(kwarg["student"])
        if kwarg["paid_by"]:
            kwarg["paid_by"] = str(kwarg["paid_by"])
        payments.append(m.Payment(**kwarg))
    return payments


def enrich_payment(session: Session, payment: m.Payment) -> m.Payment:
    payment_copy = payment.model_copy()
    student = get_names(session, payment.student)
    payment_copy.student = f"{student.first_name} {student.last_name}"
    if payment.paid_by:
        paid_by = get_names(session, payment.paid_by)
        payment_copy.paid_by = f"{paid_by.first_name} {paid_by.last_name}"
    return payment_copy
