from typing import Iterable

import streamlit as st

import db.parent as p
import db.student as s
import db.teacher as t
import db.user as u
import errors as e
import models as m
from const import TRANSLATIONS
from p.auth import hash_password


def _find_user(users: Iterable[m.User], user_email: str) -> m.User:
    for u in users:
        if u.email == user_email:
            return u


# All Parents
parents = p.get_all_parents(st.session_state["db_session"])
named_parents: list[m.NamedParent] = [
    u.to_named_version(st.session_state["db_session"], pp) for pp in parents
]
named_parents_dict = {f"{pp.first_name} {pp.last_name}": pp for pp in named_parents}

# All teachers
teachers = t.get_all_teachers(st.session_state["db_session"])
named_teachers: list[m.NamedTeacher] = [
    u.to_named_version(st.session_state["db_session"], tt) for tt in teachers
]
named_teachers_dict = {f"{tt.first_name} {tt.last_name}": tt for tt in named_teachers}

# All Students
students = s.get_all_students(st.session_state["db_session"])
named_students: list[m.NamedStudent] = [
    u.to_named_version(st.session_state["db_session"], ss) for ss in students
]
named_students_dict = {f"{ss.first_name} {ss.last_name}": ss for ss in named_students}

if "user" in st.session_state:
    user: m.User = st.session_state["user"]
    st.write(TRANSLATIONS["underConstruction"][st.session_state["language"]])

    with st.expander(TRANSLATIONS["assignRole"][st.session_state["language"]]):
        unassigned_users = u.get_unassigned_users(st.session_state["db_session"])
        selected_user_email = st.selectbox(
            TRANSLATIONS["user"][st.session_state["language"]],
            [u.email for u in unassigned_users],
        )
        left_column, right_column = st.columns(2)
        selected_user = _find_user(unassigned_users, selected_user_email)
        if selected_user:
            with left_column:
                st.write(selected_user.email)
            with right_column:
                user_role = st.selectbox(
                    TRANSLATIONS["assignRole"][st.session_state["language"]],
                    (m.UserRole.Parent, m.UserRole.Teacher, m.UserRole.Admin),
                )
            if st.button(TRANSLATIONS["assign"][st.session_state["language"]]):
                u.set_user_role(
                    st.session_state["db_session"], user_role, selected_user.id
                )
                match user_role:
                    case m.UserRole.Parent:
                        p.create_parent(
                            st.session_state["db_session"], selected_user.id
                        )
                    case m.UserRole.Teacher:
                        t.create_teacher(
                            st.session_state["db_session"], selected_user.id
                        )
                    case m.UserRole.Admin:
                        pass
                    case _:
                        st.error(e.UserRoleDoesNotExist())
                st.success(
                    TRANSLATIONS["assignRoleSuccess"][st.session_state["language"]]
                )
        else:
            st.write(TRANSLATIONS["allRolesAssigned"][st.session_state["language"]])

    with st.expander(TRANSLATIONS["createStudent"][st.session_state["language"]]):
        selected_parent = st.selectbox(
            TRANSLATIONS["parent"][st.session_state["language"]],
            named_parents_dict.keys(),
        )
        first_name = st.text_input(
            TRANSLATIONS["firstName"][st.session_state["language"]]
        )
        last_name = st.text_input(
            TRANSLATIONS["lastName"][st.session_state["language"]]
        )
        if st.button(TRANSLATIONS["create"][st.session_state["language"]]):
            fake_email = f"{first_name} {last_name}".lower().replace(" ", "_")
            hashed_password, salt = hash_password(fake_email)
            u.create_user(
                st.session_state["db_session"], fake_email, hashed_password, salt
            )
            user_student = u.get_user_by_email(
                st.session_state["db_session"], fake_email
            )
            u.update_user(
                st.session_state["db_session"],
                user_student.id,
                {
                    "first_name": first_name,
                    "last_name": last_name,
                    "role": m.UserRole.Student.value,
                },
            )
            s.create_student(
                st.session_state["db_session"],
                user_student.id,
                [named_parents_dict[selected_parent].user_id],
            )
            st.success(
                TRANSLATIONS["createStudentSuccess"][st.session_state["language"]]
            )

    with st.expander(TRANSLATIONS["assignStudents"][st.session_state["language"]]):
        selected_teacher = st.selectbox(
            TRANSLATIONS["teacher"][st.session_state["language"]],
            named_teachers_dict.keys(),
        )
        selected_students = st.multiselect(
            TRANSLATIONS["student"][st.session_state["language"]],
            named_students_dict.keys(),
        )
        if st.button(TRANSLATIONS["assign"][st.session_state["language"]]):
            t.assign_students(
                st.session_state["db_session"],
                named_teachers_dict[selected_teacher].user_id,
                [named_students_dict[ss].user_id for ss in selected_students],
            )
            st.success(
                TRANSLATIONS["assignStudentsSuccess"][st.session_state["language"]]
            )
