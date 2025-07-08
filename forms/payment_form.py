# forms/payment_form.py

import streamlit as st
from datetime import date, timedelta
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import math

def render():
    st.header("💳 Payment Agreement Form")

    with st.form("payment_form"):
        st.subheader("Borrower Info")
        name = st.text_input("Borrower's Full Name")
        address = st.text_input("Mailing Address")

        st.subheader("Agreement Terms")
        debt_amount = st.number_input("Total Debt Amount ($)", min_value=0.0, format="%.2f")
        start_date = st.date_input("First Payment Due Date", date.today())

        freq = st.selectbox(
            "Payment Frequency",
            ["Weekly", "Biweekly", "Bimonthly", "Monthly"]
        )

        sig_date = st.date_input("Agreement Signed On", date.today())

        note = st.text_area("Additional Notes (optional)", height=100)

        submitted = st.form_submit_button("Submit")

    if submitted:
        # --- Frequency mapping ---
        freq_map = {
            "Weekly": 7,
            "Biweekly": 14,
            "Bimonthly": 15,
            "Monthly": 30
        }

        interval_days = freq_map[freq]
        total_payments = 10  # default to 10 payments unless better logic needed
        est_payment = round(debt_amount / total_payments, 2)

        # Build payment schedule breakdown
        current_date = start_date
        remaining = debt_amount
        schedule = []

        while remaining > 0:
            amount = round(min(est_payment, remaining), 2)
            schedule.append({
                "date": current_date,
                "amount": amount,
                "status": "Unpaid",
                "receipt": ""
            })
            remaining -= amount
            current_date += timedelta(days=interval_days)

        total_payments = len(schedule)
        avg_payment = round(debt_amount / total_payments, 2)

        # Show schedule preview
        st.subheader("📅 Payment Plan Preview")
        st.write(f"**Estimated {total_payments} payments of about ${avg_payment} each**")

        preview_data = {
            "Due Date": [p["date"] for p in schedule],
            "Amount": [f"${p['amount']:.2f}" for p in schedule],
            "Status": [p["status"] for p in schedule],
            "Receipt #": [p["receipt"] for p in schedule]
        }
        st.table(preview_data)

        # --- Save to Google Sheets ---
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        import json
        creds = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(st.secrets["gcp_service_account"]), scope)

        client = gspread.authorize(creds)

        # 1. Save summary to Payments tab
        payments_sheet = client.open("Dealer_academy_records").worksheet("Payments")

        summary_row = [
            name,
            address,
            f"${debt_amount:,.2f}",
            str(start_date),
            freq,
            f"{total_payments} payments @ ~${avg_payment}",
            str(sig_date),
            note,
            str(date.today())
        ]
        payments_sheet.append_row(summary_row)

        # 2. Save breakdown to Payment_Tracking tab
        tracking_sheet = client.open("Dealer_academy_records").worksheet("Payment_Tracking")

        for p in schedule:
            tracking_row = [
                name,
                str(p["date"]),
                f"${p['amount']:.2f}",
                p["status"],
                p["receipt"]
            ]
            tracking_sheet.append_row(tracking_row)

        st.success("✅ Payment agreement and full plan submitted!")
