import streamlit as st

import db.user as u
import models as m
from const import TRANSLATIONS


def show_finish_register_page():
    st.title(TRANSLATIONS["finishRegister"][st.session_state["language"]])
    first_name = st.text_input(TRANSLATIONS["firstName"][st.session_state["language"]])
    last_name = st.text_input(TRANSLATIONS["lastName"][st.session_state["language"]])
    if st.button(TRANSLATIONS["update"][st.session_state["language"]]):
        user: m.User = st.session_state["user"]
        try:
            u.update_user(
                st.session_state["db_session"],
                user.id,
                {"first_name": first_name, "last_name": last_name},
            )
            st.success(TRANSLATIONS["userUpdated"][st.session_state["language"]])
            st.session_state["user"] = u.get_user_by_id(
                st.session_state["db_session"], user.id
            )
            st.rerun()
        except Exception as e:
            st.error(e)
