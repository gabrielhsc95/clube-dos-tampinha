from datetime import date, timedelta

import pandas as pd
import streamlit as st

import db.authorization as a
import db.parent as p
import db.student as s
import db.user as u
import models as m
from const import TRANSLATIONS

if "user" in st.session_state:
    user: m.User = st.session_state["user"]
    parent = p.get_parent(st.session_state["db_session"], user.id)
    st.write(TRANSLATIONS["underConstruction"][st.session_state["language"]])

    with st.expander(TRANSLATIONS["seeAuthorization"][st.session_state["language"]]):
        start_date = st.date_input(
            TRANSLATIONS["startDate"][st.session_state["language"]],
            value=date.today() - timedelta(days=30),
        )
        end_date = st.date_input(
            TRANSLATIONS["endDate"][st.session_state["language"]],
        )
        authorizations = a.get_all_authorizations_by_receiver(
            st.session_state["db_session"], user.id
        )
        authorizations = [
            a.enrich_authorization(st.session_state["db_session"], cc)
            for cc in authorizations
        ]
        authorizations_df = pd.DataFrame([cc.model_dump() for cc in authorizations])
        if not authorizations_df.empty:
            for id in authorizations_df["id"]:
                a.view_authorization(st.session_state["db_session"], id)
            authorizations_df = authorizations_df.drop(
                columns=["receiver", "is_viewed"]
            )
            authorizations_df = authorizations_df[
                (authorizations_df["sent_at"] >= start_date)
                & (authorizations_df["sent_at"] <= end_date)
            ]
            authorizations_df = authorizations_df.sort_values(
                by="sent_at", ascending=False
            )
            authorizations_df = authorizations_df.rename(
                columns={
                    "sender": TRANSLATIONS["from"][st.session_state["language"]],
                    "content": TRANSLATIONS["message"][st.session_state["language"]],
                    "sent_at": TRANSLATIONS["sent"][st.session_state["language"]],
                    "is_confirmed": TRANSLATIONS["confirmed"][
                        st.session_state["language"]
                    ],
                }
            )
        selected_authorization = st.dataframe(
            authorizations_df,
            hide_index=True,
            on_select="rerun",
            selection_mode="single-row",
            column_order=[
                TRANSLATIONS["from"][st.session_state["language"]],
                TRANSLATIONS["message"][st.session_state["language"]],
                TRANSLATIONS["sent"][st.session_state["language"]],
                TRANSLATIONS["confirmed"][st.session_state["language"]],
            ],
        )

        if selected_authorization["selection"]["rows"]:
            aa = authorizations_df.iloc[selected_authorization["selection"]["rows"]]
            st.write(TRANSLATIONS["confirmMessage"][st.session_state["language"]])
            st.write(aa[TRANSLATIONS["message"][st.session_state["language"]]][0])
            signature = st.text_input(
                TRANSLATIONS["signature"][st.session_state["language"]]
            )
            if st.button(TRANSLATIONS["confirm"][st.session_state["language"]]):
                if signature.lower() == f"{user.first_name} {user.last_name}".lower():
                    a.confirm_authorization(st.session_state["db_session"], aa["id"][0])
                    st.success(
                        TRANSLATIONS["authorizationConfirmed"][
                            st.session_state["language"]
                        ]
                    )
                else:
                    st.error(
                        TRANSLATIONS["wrongSignature"][st.session_state["language"]]
                    )
