from datetime import date, timedelta

import pandas as pd
import streamlit as st

import db.parent as p
import db.payment as pay
import db.student as s
import db.user as u
import models as m
from const import TRANSLATIONS

if "user" in st.session_state:
    user: m.User = st.session_state["user"]
    parent = p.get_parent(st.session_state["db_session"], user.id)
    st.write(TRANSLATIONS["underConstruction"][st.session_state["language"]])

    with st.expander(TRANSLATIONS["viewInvoice"][st.session_state["language"]]):
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
        payments = pay.get_all_payments_by_student(
            st.session_state["db_session"],
            named_students_dict[selected_student].user_id,
        )
        payments = [
            pay.enrich_payment(st.session_state["db_session"], pp) for pp in payments
        ]
        payments_df = pd.DataFrame([pp.model_dump() for pp in payments])
        if not payments_df.empty:
            payments_df = payments_df.drop(columns=["id"])
            payments_df = payments_df[
                (payments_df["due_date"] >= start_date)
                & (payments_df["due_date"] <= end_date)
            ]
            payments_df = payments_df.sort_values(by="due_date", ascending=False)
            payments_df = payments_df.rename(
                columns={
                    "value": TRANSLATIONS["value"][st.session_state["language"]],
                    "due_date": TRANSLATIONS["dueDate"][st.session_state["language"]],
                    "status": TRANSLATIONS["status"][st.session_state["language"]],
                    "payment_date": TRANSLATIONS["paymentDate"][
                        st.session_state["language"]
                    ],
                    "paid_by": TRANSLATIONS["paidBy"][st.session_state["language"]],
                    "reason": TRANSLATIONS["message"][st.session_state["language"]],
                    "student": TRANSLATIONS["student"][st.session_state["language"]],
                }
            )
        st.dataframe(payments_df, hide_index=True)
