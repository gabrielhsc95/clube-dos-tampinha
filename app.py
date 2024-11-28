import streamlit as st
from st_pages import get_nav_from_toml

import pages.auth as auth
import models as m
import pages.welcome as welcome
import pages.finish_register as finish_register

from const import TRANSLATIONS, LANGUAGE_MAP
from db.session import create_session


st.session_state["language"] = "en"
nav = get_nav_from_toml("pages_init.toml")
pg = st.navigation(nav, position="hidden")
pg.run()

if "db_session" not in st.session_state:
    session = create_session()
    st.session_state["db_session"] = session


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
        finish_register.show_finish_register_page()
    else:
        if user.role == m.UserRole.Admin:
            if st.session_state["language"] == "en":
                nav = get_nav_from_toml("pages_admin_en.toml")
                pg = st.navigation(nav)
                pg.run()
            elif st.session_state["language"] == "pt-br":
                nav = get_nav_from_toml("pages_admin_pt_br.toml")
                pg = st.navigation(nav)
                pg.run()
