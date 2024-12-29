from datetime import date, timedelta

import pandas as pd
import streamlit as st

import db.activity as a
import db.parent as p
import db.student as s
import db.teacher as t
import db.user as u
import models as m
from const import TRANSLATIONS

if "user" in st.session_state:
    user: m.User = st.session_state["user"]
    parent = p.get_parent(st.session_state["db_session"], user.id)
    st.write(TRANSLATIONS["underConstruction"][st.session_state["language"]])

    with st.expander(TRANSLATIONS["seeActivities"][st.session_state["language"]]):
        start_date = st.date_input(
            TRANSLATIONS["startDate"][st.session_state["language"]],
            value=date.today() - timedelta(days=30),
        )
        end_date = st.date_input(
            TRANSLATIONS["endDate"][st.session_state["language"]],
        )
        children_from_parent = []
        for student_id in parent.children:
            student = s.get_student(st.session_state["db_session"], student_id)
            named_student = u.to_named_version(st.session_state["db_session"], student)
            children_from_parent.append(named_student)
        named_students_dict = {
            f"{ss.first_name} {ss.last_name}": ss for ss in children_from_parent
        }
        selected_student = st.selectbox(
            TRANSLATIONS["student"][st.session_state["language"]],
            named_students_dict.keys(),
        )
        activities = a.get_activities_by_student(
            st.session_state["db_session"],
            named_students_dict[selected_student].user_id,
        )
        activities_df = pd.DataFrame([aa.model_dump() for aa in activities])
        if not activities_df.empty:
            activities_df = activities_df.drop(columns=["id", "student"])
            activities_df = activities_df[
                (activities_df["date"] >= start_date)
                & (activities_df["date"] <= end_date)
            ]
            teacher_names = []
            for tt in activities_df["responsible_teacher"]:
                named = u.get_names(st.session_state["db_session"], tt)
                teacher_names.append(f"{named.first_name} {named.last_name}")
            activities_df["responsible_teacher"] = teacher_names
            activities_df = activities_df.rename(
                columns={
                    "date": TRANSLATIONS["date"][st.session_state["language"]],
                    "grade": TRANSLATIONS["grade"][st.session_state["language"]],
                    "title": TRANSLATIONS["title"][st.session_state["language"]],
                    "report": TRANSLATIONS["report"][st.session_state["language"]],
                    "responsible_teacher": TRANSLATIONS["teacher"][
                        st.session_state["language"]
                    ],
                }
            )
        st.dataframe(activities_df, hide_index=True)
