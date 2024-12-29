from datetime import date, timedelta

import pandas as pd
import streamlit as st

import db.authorization as a
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

# All Authorizations
authorizations = a.get_all_authorizations(st.session_state["db_session"])
authorizations = [
    a.enrich_authorization(st.session_state["db_session"], aa) for aa in authorizations
]


if "user" in st.session_state:
    user: m.User = st.session_state["user"]
    st.write(TRANSLATIONS["underConstruction"][st.session_state["language"]])

    with st.expander(TRANSLATIONS["sendAuthorization"][st.session_state["language"]]):
        selected_parents = st.multiselect(
            TRANSLATIONS["to"][st.session_state["language"]],
            named_parents_dict.keys(),
        )
        content = st.text_input(TRANSLATIONS["message"][st.session_state["language"]])
        if st.button(TRANSLATIONS["send"][st.session_state["language"]]):
            for pp in selected_parents:
                a.create_authorization(
                    st.session_state["db_session"],
                    user.id,
                    named_parents_dict[pp].user_id,
                    content,
                )
            st.success(
                TRANSLATIONS["sendAuthorizationSuccess"][st.session_state["language"]]
            )

    with st.expander(TRANSLATIONS["seeAuthorization"][st.session_state["language"]]):
        start_date = st.date_input(
            TRANSLATIONS["startDate"][st.session_state["language"]],
            value=date.today() - timedelta(days=30),
        )
        end_date = st.date_input(
            TRANSLATIONS["endDate"][st.session_state["language"]],
        )
        authorizations_df = pd.DataFrame([cc.model_dump() for cc in authorizations])
        if not authorizations_df.empty:
            authorizations_df = authorizations_df.drop(columns=["id"])
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
                    "receiver": TRANSLATIONS["to"][st.session_state["language"]],
                    "content": TRANSLATIONS["message"][st.session_state["language"]],
                    "sent_at": TRANSLATIONS["sent"][st.session_state["language"]],
                    "is_viewed": TRANSLATIONS["viewed"][st.session_state["language"]],
                    "is_confirmed": TRANSLATIONS["confirmed"][
                        st.session_state["language"]
                    ],
                }
            )
        st.dataframe(authorizations_df, hide_index=True)
