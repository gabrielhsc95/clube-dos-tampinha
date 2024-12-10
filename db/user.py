from typing import Dict, Iterable, Union

from cassandra.cluster import Session

import errors as e
import models as m
from const import KEY_SPACE


def get_complete_user(session: Session, email: str) -> m.CompleteUser:
    result = session.execute(
        f"""
        SELECT * 
        FROM {KEY_SPACE}.user 
        WHERE email='{email}' 
        ALLOW FILTERING;
        """
    )
    first_result = result.one()
    if first_result is None:
        raise e.UserDoesNotExist()
    kwarg = {k: getattr(first_result, k) for k in result.column_names}
    kwarg["id"] = str(kwarg["id"])
    return m.CompleteUser(**kwarg)


def get_user_by_email(session: Session, email: str) -> m.User:
    result = session.execute(
        f"""
        SELECT id, email, first_name, last_name, role 
        FROM {KEY_SPACE}.user
        WHERE email='{email}' 
        ALLOW FILTERING;
        """
    )
    first_result = result.one()
    if first_result is None:
        raise e.UserDoesNotExist()
    kwarg = {k: getattr(first_result, k) for k in result.column_names}
    kwarg["id"] = str(kwarg["id"])
    return m.User(**kwarg)


def get_user_by_id(session: Session, id: str) -> m.User:
    result = session.execute(
        f"""
        SELECT id, email, first_name, last_name, role 
        FROM {KEY_SPACE}.user 
        WHERE id={id};
        """
    )
    first_result = result.one()
    if first_result is None:
        raise e.UserDoesNotExist()
    kwarg = {k: getattr(first_result, k) for k in result.column_names}
    kwarg["id"] = str(kwarg["id"])
    return m.User(**kwarg)


def create_user(session: Session, email: str, hashed_password: str, salt: str):
    try:
        get_user_by_email(session, email)
        raise e.UserAlreadyExists()
    except e.UserDoesNotExist:
        session.execute(
            f"""
            INSERT INTO {KEY_SPACE}.user 
                (id    , email    , password           , salt    , first_name, last_name, role)
            VALUES 
                (uuid(), '{email}', '{hashed_password}', '{salt}', null      , null     , 'n/a');
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


def get_unassigned_users(session: Session) -> Iterable[m.User]:
    users_db = session.execute(
        f"""
        SELECT id, email, first_name, last_name, role 
        FROM {KEY_SPACE}.user 
        WHERE role='n/a'
         ALLOW FILTERING;
        """
    )
    users = []
    for u in users_db:
        kwarg = {k: getattr(u, k) for k in users_db.column_names}
        kwarg["id"] = str(kwarg["id"])
        users.append(m.User(**kwarg))
    return users


def set_user_role(session: Session, role: m.UserRole, user_id: str):
    session.execute(
        f"""
        UPDATE {KEY_SPACE}.user
        SET role = '{role.value}'
        WHERE id = {user_id};
        """
    )


def get_names(session: Session, user_id: str) -> m.Named:
    result = session.execute(
        f"""
        SELECT first_name, last_name
        FROM {KEY_SPACE}.user
        WHERE id = {user_id};
        """
    )
    first_result = result.one()
    if first_result is None:
        # it should probably not end up here tho.
        raise e.UserDoesNotExist()
    return m.Named(
        first_name=first_result.first_name,
        last_name=first_result.last_name,
    )


def to_named_version(
    session: Session, model: Union[m.Parent, m.Student, m.Teacher]
) -> Union[m.NamedParent, m.NamedStudent, m.NamedTeacher]:
    model_map = {
        m.Parent: m.NamedParent,
        m.Student: m.NamedStudent,
        m.Teacher: m.NamedTeacher,
    }
    name = get_names(session, model.user_id)
    kwargs = {**name.model_dump(), **model.model_dump()}
    return model_map.get(model.__class__)(**kwargs)
