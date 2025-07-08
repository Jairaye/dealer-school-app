# forms/assessment_form.py

import streamlit as st
from datetime import date
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

SKILL_AREAS = [
    "Deck Setup",
    "Shuffle Process",
    "Card Delivery",
    "Hand Reading",
    "Reading a Low Hand",
    "Layout",
    "Stud",
    "Big O",
    "Draw"
]

RATINGS = ["Below Standards", "Met Standards", "Exceeded Standards"]

def render():
    st.header("📋 Student Assessment")

    # Connect to Google Sheets
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)

    # Get student list from Enrollment sheet
    sheet_enroll = client.open("Dealer_academy_records").worksheet("Enrollment")
    df_enroll = pd.DataFrame(sheet_enroll.get_all_records())

    if df_enroll.empty or "Student ID" not in df_enroll.columns:
        st.error("Enrollment data not found or missing 'Student ID' column.")
        return

    df_enroll["Display"] = df_enroll["Student ID"] + " - " + df_enroll["First Name"] + " " + df_enroll["Last Name"]
    selected = st.selectbox("Select Student", df_enroll["Display"].tolist())

    student_id = selected.split(" - ")[0]

    col1, col2 = st.columns(2)
    with col1:
        init_date = st.date_input("Initial Assessment Date")
    with col2:
        final_date = st.date_input("Final Assessment Date")

    st.markdown("---")
    st.subheader("Skill Ratings")

    init_scores = {}
    final_scores = {}

    for skill in SKILL_AREAS:
        st.markdown(f"**{skill}**")
        col1, col2 = st.columns(2)

        with col1:
            init_scores[skill] = st.radio(f"Initial - {skill}", RATINGS, horizontal=True, key=f"init_{skill}")
        with col2:
            final_scores[skill] = st.radio(f"Final - {skill}", RATINGS, horizontal=True, key=f"final_{skill}")

        st.markdown("---")

    if st.button("Submit Assessment"):
        # Prepare data row
        row = [student_id, str(init_date), str(final_date)]
        for skill in SKILL_AREAS:
            row.append(init_scores[skill])
            row.append(final_scores[skill])
        row.append(str(date.today()))

        # Write to Assessments sheet
        assess_sheet = client.open("Dealer_academy_records").worksheet("Assessments")

        headers = ["Student ID", "Initial Date", "Final Date"]
        for skill in SKILL_AREAS:
            headers.append(f"{skill} (Initial)")
            headers.append(f"{skill} (Final)")
        headers.append("Submitted On")

        existing = assess_sheet.get_all_records()
        if not existing:
            assess_sheet.append_row(headers)

        assess_sheet.append_row(row)
        st.success("Assessment submitted successfully.")
