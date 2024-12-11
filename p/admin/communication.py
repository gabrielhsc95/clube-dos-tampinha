import streamlit as st

import db.communication as c
import db.parent as p
import db.user as u
import models as m
from const import TRANSLATIONS

# All Parents
parents = p.get_all_parents(st.session_state["db_session"])
named_parents: list[m.NamedParent] = [
    u.to_named_version(st.session_state["db_session"], pp) for pp in parents
]
named_parents_dict = {f"{pp.first_name} {pp.last_name}": pp for pp in named_parents}

if "user" in st.session_state:
    user: m.User = st.session_state["user"]
    st.write(TRANSLATIONS["underConstruction"][st.session_state["language"]])

    with st.expander(TRANSLATIONS["sendCommunication"][st.session_state["language"]]):
        selected_parents = st.multiselect(
            TRANSLATIONS["to"][st.session_state["language"]],
            named_parents_dict.keys(),
        )
        content = st.text_input(TRANSLATIONS["message"][st.session_state["language"]])
        if st.button(TRANSLATIONS["send"][st.session_state["language"]]):
            for pp in selected_parents:
                c.create_communication(
                    st.session_state["db_session"],
                    user.id,
                    named_parents_dict[pp].user_id,
                    content,
                )
            st.success(
                TRANSLATIONS["sendCommunicationSuccess"][st.session_state["language"]]
            )
