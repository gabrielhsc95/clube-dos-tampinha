from typing import Dict

from cassandra.cluster import Session

import errors as e
import models as m
from const import KEY_SPACE


def get_complete_user(session: Session, email: str) -> m.CompleteUser:
    result = session.execute(
        f"SELECT * FROM {KEY_SPACE}.user WHERE email='{email}' ALLOW FILTERING;"
    )
    first_result = result.one()
    if first_result is None:
        raise e.UserDoesNotExist()
    kwarg = {k: getattr(first_result, k) for k in result.column_names}
    kwarg["id"] = str(kwarg["id"])
    return m.CompleteUser(**kwarg)


def get_user_by_email(session: Session, email: str) -> m.User:
    result = session.execute(
        f"SELECT id, email, first_name, last_name, role FROM {KEY_SPACE}.user WHERE email='{email}' ALLOW FILTERING;"
    )
    first_result = result.one()
    if first_result is None:
        raise e.UserDoesNotExist()
    kwarg = {k: getattr(first_result, k) for k in result.column_names}
    kwarg["id"] = str(kwarg["id"])
    return m.User(**kwarg)


def get_user_by_id(session: Session, id: str) -> m.User:
    result = session.execute(
        f"SELECT id, email, first_name, last_name, role FROM {KEY_SPACE}.user WHERE id='={id};"
    )
    first_result = result.one()
    if first_result is None:
        raise e.UserDoesNotExist()
    kwarg = {k: getattr(first_result, k) for k in result.column_names}
    kwarg["id"] = str(kwarg["id"])
    return m.User(**kwarg)


def register_user(session: Session, email: str, hashed_password: str, salt: str):
    user = get_user_by_email(session, email)
    if user is not None:
        raise e.UserAlreadyExists()
    session.execute(
        f"""
        INSERT INTO {KEY_SPACE}.user 
            (id    , email    , password           , salt    , first_name, last_name, role)
        VALUES 
            (uuid(), '{email}', '{hashed_password}', '{salt}', null      , null     , null);
        """
    )


def update_user(session: Session, user_id: str, updates: Dict[str, str]):
    session.execute(
        f"""
        UPDATE {KEY_SPACE}.user
        SET {", ".join([f"{k} = '{v}'" for k, v in updates.items()])}
        WHERE id={user_id};
        """
    )
