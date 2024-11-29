from typing import Iterable

import streamlit as st

import db.parent as p
import db.teacher as t
import db.user as u
import errors as e
import models as m
from const import TRANSLATIONS


def _find_user(users: Iterable[m.User], user_email: str) -> m.User:
    for u in users:
        if u.email == user_email:
            return u


if "user" in st.session_state:
    user: m.User = st.session_state["user"]
    st.write(TRANSLATIONS["underConstruction"][st.session_state["language"]])

    with st.expander(TRANSLATIONS["assignRole"][st.session_state["language"]]):
        unassigned_users = u.get_unassigned_users(st.session_state["db_session"])
        selected_user_email = st.selectbox(
            TRANSLATIONS["user"][st.session_state["language"]],
            [u.email for u in unassigned_users],
        )
        left_column, right_column = st.columns(2)
        selected_user = _find_user(unassigned_users, selected_user_email)
        if selected_user:
            with left_column:
                st.write(selected_user.email)
            with right_column:
                user_role = st.selectbox(
                    TRANSLATIONS["assignRole"][st.session_state["language"]],
                    (m.UserRole.Parent, m.UserRole.Teacher, m.UserRole.Admin),
                )
            if st.button(TRANSLATIONS["assign"][st.session_state["language"]]):
                u.set_user_role(
                    st.session_state["db_session"], user_role, selected_user.id
                )
                match user_role:
                    case m.UserRole.Parent:
                        p.create_parent(
                            st.session_state["db_session"], selected_user.id
                        )
                    case m.UserRole.Teacher:
                        t.create_teacher(
                            st.session_state["db_session"], selected_user.id
                        )
                    case m.UserRole.Admin:
                        pass
                    case _:
                        st.error(e.UserRoleDoesNotExist())
        else:
            st.write(TRANSLATIONS["allRolesAssigned"][st.session_state["language"]])
