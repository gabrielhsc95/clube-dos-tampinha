from datetime import date, timedelta

import pandas as pd
import streamlit as st

import db.activity as a
import db.student as s
import db.teacher as t
import db.user as u
import models as m
from const import TRANSLATIONS

# All Teachers
teachers = t.get_all_teachers(st.session_state["db_session"])
named_teachers: list[m.NamedTeacher] = [
    u.to_named_version(st.session_state["db_session"], tt) for tt in teachers
]
named_teachers_dict = {f"{tt.first_name} {tt.last_name}": tt for tt in named_teachers}


if "user" in st.session_state:
    user: m.User = st.session_state["user"]
    st.write(TRANSLATIONS["underConstruction"][st.session_state["language"]])

    with st.expander(TRANSLATIONS["seeActivities"][st.session_state["language"]]):
        start_date = st.date_input(
            TRANSLATIONS["startDate"][st.session_state["language"]],
            value=date.today() - timedelta(days=30),
        )
        end_date = st.date_input(
            TRANSLATIONS["endDate"][st.session_state["language"]],
        )
        selected_teacher = st.selectbox(
            TRANSLATIONS["teacher"][st.session_state["language"]],
            named_teachers_dict.keys(),
        )
        students_from_teacher = []
        for student_id in named_teachers_dict[selected_teacher].students:
            student = s.get_student(st.session_state["db_session"], student_id)
            named_student = u.to_named_version(st.session_state["db_session"], student)
            students_from_teacher.append(named_student)
        named_students_dict = {
            f"{ss.first_name} {ss.last_name}": ss for ss in students_from_teacher
        }
        selected_student = st.selectbox(
            TRANSLATIONS["student"][st.session_state["language"]],
            named_students_dict.keys(),
        )
        activities = a.get_activities(
            st.session_state["db_session"],
            named_students_dict[selected_student].user_id,
            named_teachers_dict[selected_teacher].user_id,
        )
        activities_df = pd.DataFrame([aa.model_dump() for aa in activities])
        if not activities_df.empty:
            activities_df = activities_df.drop(
                columns=["id", "responsible_teacher", "student"]
            )
            activities_df = activities_df[
                (activities_df["date"] >= start_date)
                & (activities_df["date"] <= end_date)
            ]
        st.dataframe(activities_df, hide_index=True)
