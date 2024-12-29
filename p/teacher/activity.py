import pandas as pd
import streamlit as st

import db.activity as a
import db.student as s
import db.teacher as t
import db.user as u
import models as m
from const import TRANSLATIONS

if "user" in st.session_state:
    user: m.User = st.session_state["user"]
    teacher = t.get_teacher(st.session_state["db_session"], user.id)
    st.write(TRANSLATIONS["underConstruction"][st.session_state["language"]])

    with st.expander(TRANSLATIONS["logActivity"][st.session_state["language"]]):
        students_from_teacher = []
        for student_id in teacher.students:
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
        date = st.date_input(
            TRANSLATIONS["date"][st.session_state["language"]],
        )
        title = st.text_input(TRANSLATIONS["title"][st.session_state["language"]])
        grade = st.slider(
            TRANSLATIONS["grade"][st.session_state["language"]], 0.0, 10.0, 10.0, 0.1
        )
        report = st.text_area(TRANSLATIONS["report"][st.session_state["language"]])
        if st.button(TRANSLATIONS["submit"][st.session_state["language"]]):
            a.create_activity(
                st.session_state["db_session"],
                teacher.user_id,
                date,
                named_students_dict[selected_student].user_id,
                grade,
                title,
                report,
            )
            st.success(TRANSLATIONS["logActivitySuccess"][st.session_state["language"]])
