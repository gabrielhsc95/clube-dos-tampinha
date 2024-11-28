import streamlit as st

import auth
import models as m
import welcome
from const import TRANSLATIONS, LANGUAGE_MAP
from db.session import create_session

session = create_session()
st.session_state["db_session"] = session
st.session_state["language"] = "en"

st.title("Clube dos Tampinha")
language = st.selectbox(
    TRANSLATIONS["language"][st.session_state["language"]],
    ("English", "Português"),
)
st.session_state["language"] = LANGUAGE_MAP.get(language)


if "user" not in st.session_state:
    auth.show_login_page()
else:
    user: m.User = st.session_state["user"]
    if user.first_name is None:
        welcome.show_finish_register_page()
    else:
        welcome.show_welcome_page()
