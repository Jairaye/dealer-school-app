import streamlit as st
from datetime import date
from utils.gspread_loader import load_sheet_client  # ✅ Sheet client shortcut

def render():
    st.header("💸 Log a Tuition Payment")

    client = load_sheet_client()
    sheet = client.open("Dealer_academy_records").worksheet("Payment_Tracking")

    with st.form("payment_entry"):
        st.subheader("Payment Info")
        col1, col2 = st.columns(2)
        borrower = col1.text_input("Student Name")
        due_date = col2.date_input("Due Date", value=date.today())

        col3, col4 = st.columns(2)
        amount = col3.text_input("Amount (e.g. $495.00)")
        receipt = col4.text_input("Receipt Number")

        status = st.radio("Payment Status", ["Paid", "Unpaid"], horizontal=True)

        submit = st.form_submit_button("Submit Payment")

    if submit:
        row = [
            borrower,
            due_date.strftime("%Y-%m-%d"),
            amount,
            status,
            receipt,
            date.today().strftime("%Y-%m-%d")
        ]

        headers = ["Borrower", "Due Date", "Amount", "Status", "Receipt #", "Submitted On"]

        existing = sheet.get_all_records()
        if not existing:
            sheet.append_row(headers)

        sheet.append_row(row)
        st.success(f"✅ Payment logged for {borrower}")