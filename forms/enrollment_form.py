import streamlit as st
from datetime import date
import pandas as pd
import random
from utils.gspread_loader import load_sheet_client  # 🌟 Modular credential loader

def generate_student_id(existing_ids):
    year = str(date.today().year)[-2:]  # '25'
    initials = "JR"  # Customize if needed
    prefix = f"VCD-{year}-{initials}"

    while True:
        rand_digits = f"{random.randint(0, 9999):04d}"
        full_id = f"{prefix}-{rand_digits}"
        if full_id not in existing_ids:
            return full_id

def render():
    st.header("📝 Enrollment Form")

    client = load_sheet_client()  # 🔌 Single call to get Sheets access
    sheet = client.open("Dealer_academy_records").worksheet("Enrollment")

    existing_data = sheet.get_all_records()
    existing_ids = {row.get("Student ID") for row in existing_data if "Student ID" in row}

    with st.form("enrollment_form"):
        st.subheader("Student Info")
        col1, col2 = st.columns(2)
        first = col1.text_input("First Name")
        last = col2.text_input("Last Name")

        street = st.text_input("Street Address")
        col3, col4, col5 = st.columns([3, 1, 2])
        state = col4.text_input("State")
        zip_code = col5.text_input("Zip Code")

        phone = st.text_input("Preferred Phone Number")
        email = st.text_input("Email Address")

        st.markdown("**Course Name:** Professional Poker Dealing")
        st.markdown("**Course Length:** 120 hours")
        st.markdown("**Tuition Cost:** $1,495.00")
        start_date = st.date_input("Start Date", date.today())

        st.subheader("Emergency Contact")
        ec_first = st.text_input("Emergency First Name")
        ec_last = st.text_input("Emergency Last Name")
        ec_phone = st.text_input("Emergency Phone")
        ec_relation = st.text_input("Relationship to Student")

        submitted = st.form_submit_button("Submit")

    if submitted:
        student_id = generate_student_id(existing_ids)

        row = [
            student_id, first, last, street, state, zip_code,
            phone, email, start_date.strftime("%Y-%m-%d"),
            ec_first, ec_last, ec_phone, ec_relation,
            date.today().strftime("%Y-%m-%d")
        ]

        headers = [
            "Student ID", "First Name", "Last Name", "Street Address", "State", "Zip Code",
            "Phone", "Email", "Start Date",
            "Emergency First", "Emergency Last", "Emergency Phone", "Emergency Relationship",
            "Submitted On"
        ]

        if not existing_data:
            sheet.append_row(headers)

        sheet.append_row(row)
        st.success(f"✅ Student {first} {last} enrolled with ID: {student_id}")