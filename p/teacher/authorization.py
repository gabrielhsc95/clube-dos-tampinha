from datetime import date, timedelta

import pandas as pd
import streamlit as st

import db.authorization as a
import db.student as s
import db.teacher as t
import db.user as u
import models as m
from const import TRANSLATIONS

if "user" in st.session_state:
    user: m.User = st.session_state["user"]
    teacher = t.get_teacher(st.session_state["db_session"], user.id)
    st.write(TRANSLATIONS["underConstruction"][st.session_state["language"]])

    with st.expander(TRANSLATIONS["sendAuthorization"][st.session_state["language"]]):
        students = [
            s.get_student(st.session_state["db_session"], student_id)
            for student_id in teacher.students
        ]
        named_students: list[m.NamedStudent] = [
            u.to_named_version(st.session_state["db_session"], ss) for ss in students
        ]
        named_students_dict = {
            f"{tt.first_name} {tt.last_name}": tt for tt in named_students
        }
        named_parents_dict = {}
        for ss in named_students:
            parents = []
            for pp in ss.parents:
                named = u.get_names(st.session_state["db_session"], pp)
                parents.append(f"{named.first_name} {named.last_name}")
            named_parents_dict[f"{ss.first_name} {ss.last_name}"] = parents
        options_to = [
            f"{ss} ({', '.join(named_parents_dict[ss])})" for ss in named_students_dict
        ]
        selected_to = st.multiselect(
            TRANSLATIONS["to"][st.session_state["language"]],
            options_to,
        )
        content = st.text_input(TRANSLATIONS["message"][st.session_state["language"]])
        if st.button(TRANSLATIONS["send"][st.session_state["language"]]):
            for to in selected_to:
                ss = to.split(" (")[0]
                for pp in named_students_dict[ss].parents:
                    a.create_authorization(
                        st.session_state["db_session"],
                        user.id,
                        pp,
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
        authorizations = a.get_all_authorizations_by_sender(
            st.session_state["db_session"], user.id
        )
        authorizations = [
            a.enrich_authorization(st.session_state["db_session"], cc)
            for cc in authorizations
        ]
        authorizations_df = pd.DataFrame([cc.model_dump() for cc in authorizations])
        if not authorizations_df.empty:
            authorizations_df = authorizations_df.drop(columns=["id", "sender"])
            authorizations_df = authorizations_df[
                (authorizations_df["sent_at"] >= start_date)
                & (authorizations_df["sent_at"] <= end_date)
            ]
            authorizations_df = authorizations_df.rename(
                columns={
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
