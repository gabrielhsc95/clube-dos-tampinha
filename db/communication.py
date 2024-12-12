from typing import Iterable

from cassandra.cluster import Session

import models as m
from const import KEY_SPACE
from db.user import get_names


def create_communication(
    session: Session,
    sender: str,
    receiver: str,
    content: str,
):
    session.execute(
        f"""
        INSERT INTO {KEY_SPACE}.communication 
            (id    , sender  , receiver  , content    , sent_at           , is_viewed)
        VALUES 
            (uuid(), {sender}, {receiver}, '{content}', toTimestamp(now()), false);
        """
    )


def view_communication(session: Session, id: str):
    session.execute(
        f"""
        UPDATE {KEY_SPACE}.communication
        SET is_view=true
        WHERE id={id};
        """
    )


def get_communications(session: Session, user_id: str) -> Iterable[m.Communication]:
    communications_db = session.execute(
        f"""
        SELECT *
        FROM {KEY_SPACE}.communication
        WHERE receiver={user_id}
        ALLOW FILTERING;
        """
    )
    communications = []
    for c in communications_db:
        kwarg = {k: getattr(c, k) for k in communications_db.column_names}
        kwarg["id"] = str(kwarg["id"])
        kwarg["sender"] = str(kwarg["sender"])
        kwarg["receiver"] = str(kwarg["receiver"])
        kwarg["sent_at"] = kwarg["sent_at"].date()
        communications.append(m.Communication(**kwarg))
    return communications


def get_all_communications(session: Session) -> Iterable[m.Communication]:
    communications_db = session.execute(
        f"""
        SELECT *
        FROM {KEY_SPACE}.communication;
        """
    )
    communications = []
    for c in communications_db:
        kwarg = {k: getattr(c, k) for k in communications_db.column_names}
        kwarg["id"] = str(kwarg["id"])
        kwarg["sender"] = str(kwarg["sender"])
        kwarg["receiver"] = str(kwarg["receiver"])
        kwarg["sent_at"] = kwarg["sent_at"].date()
        communications.append(m.Communication(**kwarg))
    return communications


def enrich_communication(
    session: Session, communication: m.Communication
) -> m.Communication:
    communication_copy = communication.model_copy()
    sender = get_names(session, communication.sender)
    communication_copy.sender = f"{sender.first_name} {sender.last_name}"
    receiver = get_names(session, communication.receiver)
    communication_copy.receiver = f"{receiver.first_name} {receiver.last_name}"
    return communication_copy
