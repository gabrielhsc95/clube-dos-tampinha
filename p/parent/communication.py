from datetime import date, timedelta

import pandas as pd
import streamlit as st

import db.communication as c
import db.parent as p
import db.student as s
import db.user as u
import models as m
from const import TRANSLATIONS

if "user" in st.session_state:
    user: m.User = st.session_state["user"]
    parent = p.get_parent(st.session_state["db_session"], user.id)
    st.write(TRANSLATIONS["underConstruction"][st.session_state["language"]])

    with st.expander(TRANSLATIONS["seeCommunication"][st.session_state["language"]]):
        start_date = st.date_input(
            TRANSLATIONS["startDate"][st.session_state["language"]],
            value=date.today() - timedelta(days=30),
        )
        end_date = st.date_input(
            TRANSLATIONS["endDate"][st.session_state["language"]],
        )
        communications = c.get_all_communications_by_receiver(
            st.session_state["db_session"], user.id
        )
        communications = [
            c.enrich_communication(st.session_state["db_session"], cc)
            for cc in communications
        ]
        communications_df = pd.DataFrame([cc.model_dump() for cc in communications])
        if not communications_df.empty:
            for id in communications_df["id"]:
                c.view_communication(st.session_state["db_session"], id)
            communications_df = communications_df.drop(
                columns=["id", "receiver", "is_viewed"]
            )
            communications_df = communications_df[
                (communications_df["sent_at"] >= start_date)
                & (communications_df["sent_at"] <= end_date)
            ]
            communications_df = communications_df.sort_values(
                by="sent_at", ascending=False
            )
            communications_df = communications_df.rename(
                columns={
                    "sender": TRANSLATIONS["from"][st.session_state["language"]],
                    "content": TRANSLATIONS["message"][st.session_state["language"]],
                    "sent_at": TRANSLATIONS["sent"][st.session_state["language"]],
                }
            )
        st.dataframe(communications_df, hide_index=True)
