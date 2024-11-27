import streamlit as st

import auth
from const import KEY_SPACE
from db.utils import create_session

session = create_session()
st.session_state["db_session"] = session
st.session_state["language"] = "pt-br"

st.write("Clube dos Tampinha")

if "authenticated" not in st.session_state:
    auth.show_login_page()
else:
    st.write("opa")
