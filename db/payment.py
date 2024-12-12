from datetime import date
from typing import Iterable

from cassandra.cluster import Session

import models as m
from const import KEY_SPACE


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


def get_all_payments(session: Session) -> Iterable[m.Parent]:
    payments_db = session.execute(
        f"""
        SELECT *
        FROM {KEY_SPACE}.payment
        """
    )
    payments = []
    for p in payments_db:
        kwarg = {k: getattr(p, k) for k in payments.column_names}
        payments.append(m.Payment(**kwarg))
    return payments
