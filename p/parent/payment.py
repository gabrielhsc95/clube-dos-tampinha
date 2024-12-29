import streamlit as st

import models as m
from const import TRANSLATIONS

if "user" in st.session_state:
    user: m.User = st.session_state["user"]
    st.write(TRANSLATIONS["underConstruction"][st.session_state["language"]])
