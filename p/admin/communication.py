from datetime import date, timedelta

import pandas as pd
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

# All Communications
communications = c.get_all_communications(st.session_state["db_session"])
communications = [
    c.enrich_communication(st.session_state["db_session"], cc) for cc in communications
]


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

    with st.expander(TRANSLATIONS["seeCommunication"][st.session_state["language"]]):
        start_date = st.date_input(
            TRANSLATIONS["startDate"][st.session_state["language"]],
            value=date.today() - timedelta(days=30),
        )
        end_date = st.date_input(
            TRANSLATIONS["endDate"][st.session_state["language"]],
        )
        communications_df = pd.DataFrame([cc.model_dump() for cc in communications])
        communications_df = communications_df.drop(columns=["id"])
        communications_df = communications_df[
            (communications_df["sent_at"] >= start_date)
            & (communications_df["sent_at"] <= end_date)
        ]
        communications_df = communications_df.rename(
            columns={
                "sender": TRANSLATIONS["from"][st.session_state["language"]],
                "receiver": TRANSLATIONS["to"][st.session_state["language"]],
                "content": TRANSLATIONS["message"][st.session_state["language"]],
                "sent_at": TRANSLATIONS["sent"][st.session_state["language"]],
                "is_viewed": TRANSLATIONS["viewed"][st.session_state["language"]],
            }
        )
        st.dataframe(communications_df, hide_index=True)
