from typing import Iterable

from cassandra.cluster import Session

import models as m
from const import KEY_SPACE
from db.user import get_names


def create_authorization(
    session: Session,
    sender: str,
    receiver: str,
    content: str,
):
    session.execute(
        f"""
        INSERT INTO {KEY_SPACE}.authorization 
            (id    , sender  , receiver  , content    , sent_at           , is_viewed, is_confirmed)
        VALUES 
            (uuid(), {sender}, {receiver}, '{content}', toTimestamp(now()), false    , false);
        """
    )


def view_authorization(session: Session, id: str):
    session.execute(
        f"""
        UPDATE {KEY_SPACE}.authorization
        SET is_viewed=true
        WHERE id={id};
        """
    )


def confirm_authorization(session: Session, id: str):
    session.execute(
        f"""
        UPDATE {KEY_SPACE}.authorization
        SET is_confirmed=true
        WHERE id={id};
        """
    )


def get_authorizations(session: Session, user_id: str) -> Iterable[m.Authorization]:
    authorizations_db = session.execute(
        f"""
        SELECT *
        FROM {KEY_SPACE}.authorization
        WHERE receiver={user_id}
        ALLOW FILTERING;
        """
    )
    authorizations = []
    for c in authorizations_db:
        kwarg = {k: getattr(c, k) for k in authorizations_db.column_names}
        kwarg["id"] = str(kwarg["id"])
        kwarg["sender"] = str(kwarg["sender"])
        kwarg["receiver"] = str(kwarg["receiver"])
        authorizations.append(m.Authorization(**kwarg))
    return authorizations


def get_all_authorizations(session: Session) -> Iterable[m.Authorization]:
    authorizations_db = session.execute(
        f"""
        SELECT *
        FROM {KEY_SPACE}.authorization;
        """
    )
    authorizations = []
    for c in authorizations_db:
        kwarg = {k: getattr(c, k) for k in authorizations_db.column_names}
        kwarg["id"] = str(kwarg["id"])
        kwarg["sender"] = str(kwarg["sender"])
        kwarg["receiver"] = str(kwarg["receiver"])
        kwarg["sent_at"] = kwarg["sent_at"].date()
        authorizations.append(m.Authorization(**kwarg))
    return authorizations


def get_all_authorizations_by_sender(
    session: Session, sender: str
) -> Iterable[m.Authorization]:
    authorizations_db = session.execute(
        f"""
        SELECT *
        FROM {KEY_SPACE}.authorization
        WHERE sender={sender}
        ALLOW FILTERING;
        """
    )
    authorizations = []
    for c in authorizations_db:
        kwarg = {k: getattr(c, k) for k in authorizations_db.column_names}
        kwarg["id"] = str(kwarg["id"])
        kwarg["sender"] = str(kwarg["sender"])
        kwarg["receiver"] = str(kwarg["receiver"])
        kwarg["sent_at"] = kwarg["sent_at"].date()
        authorizations.append(m.Authorization(**kwarg))
    return authorizations


def get_all_authorizations_by_receiver(
    session: Session, receiver: str
) -> Iterable[m.Authorization]:
    authorizations_db = session.execute(
        f"""
        SELECT *
        FROM {KEY_SPACE}.authorization
        WHERE receiver={receiver}
        ALLOW FILTERING;
        """
    )
    authorizations = []
    for c in authorizations_db:
        kwarg = {k: getattr(c, k) for k in authorizations_db.column_names}
        kwarg["id"] = str(kwarg["id"])
        kwarg["sender"] = str(kwarg["sender"])
        kwarg["receiver"] = str(kwarg["receiver"])
        kwarg["sent_at"] = kwarg["sent_at"].date()
        authorizations.append(m.Authorization(**kwarg))
    return authorizations


def enrich_authorization(
    session: Session, authorization: m.Authorization
) -> m.Authorization:
    authorization_copy = authorization.model_copy()
    sender = get_names(session, authorization.sender)
    authorization_copy.sender = f"{sender.first_name} {sender.last_name}"
    receiver = get_names(session, authorization.receiver)
    authorization_copy.receiver = f"{receiver.first_name} {receiver.last_name}"
    return authorization_copy
