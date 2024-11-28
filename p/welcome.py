import streamlit as st

import db.user as u
import models as m
from const import TRANSLATIONS

if "user" in st.session_state:
    user: m.User = st.session_state["user"]
    st.write(
        f"{TRANSLATIONS['welcome'][st.session_state['language']]}, {user.first_name} {user.last_name}."
    )
