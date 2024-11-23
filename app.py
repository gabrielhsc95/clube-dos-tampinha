import streamlit as st

from const import KEYSPACE
from db.utils import create_session

session = create_session()


st.write("Clube dos Tampinha")

st.write(str(session.execute(f"SELECT * FROM {KEYSPACE}.user;")))
