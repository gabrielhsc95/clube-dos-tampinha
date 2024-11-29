from typing import Tuple

import bcrypt
import streamlit as st

import db.user as u
from const import TRANSLATIONS


def hash_password(password: str) -> Tuple[str, str]:
    """Hashes the password using bcrypt."""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password.decode("utf-8"), salt.decode("utf-8")


def check_password(password: str, hashed_password: str) -> bool:
    """Checks if the provided password matches the hashed password."""
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


def show_login_page():
    st.title(TRANSLATIONS["login"][st.session_state["language"]])
    email = st.text_input(TRANSLATIONS["email"][st.session_state["language"]])
    password = st.text_input(
        TRANSLATIONS["password"][st.session_state["language"]], type="password"
    )
    left_column, right_column = st.columns(2)
    with left_column:
        if st.button(TRANSLATIONS["signin"][st.session_state["language"]]):
            hashed_password, salt = hash_password(password)
            try:
                u.create_user(
                    st.session_state["db_session"], email, hashed_password, salt
                )
                st.success(
                    TRANSLATIONS["registerSuccess"][st.session_state["language"]]
                )
            except Exception as e:
                st.error(e)

    with right_column:
        if st.button(TRANSLATIONS["login"][st.session_state["language"]]):
            user = u.get_complete_user(st.session_state["db_session"], email)
            if user.role is None:
                st.error(TRANSLATIONS["roleError"][st.session_state["language"]])
            else:
                if check_password(password, user.password):
                    st.session_state["user"] = user.to_user()
                    st.success(
                        f"{TRANSLATIONS['loginSuccess'][st.session_state['language']]} {TRANSLATIONS[user.role][st.session_state['language']]}!"
                    )
                    st.rerun()
                else:
                    st.error(TRANSLATIONS["loginError"][st.session_state["language"]])
