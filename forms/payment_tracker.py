# forms/payment_tracker.py

import streamlit as st
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

def render():
    st.header("📌 Track Payment Status")

    # Connect to Google Sheets
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)

    sheet = client.open("Dealer_academy_records").worksheet("Payment_Tracking")

    # Load payment tracking data
    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    if df.empty:
        st.info("No payment data found.")
        return

    # Search box
    st.subheader("🔍 Search")
    search_term = st.text_input("Enter Student ID, Last Name, or First Name").strip().lower()

    if search_term:
        df = df[df.apply(lambda row:
            search_term in str(row["Borrower"]).lower() or
            search_term in str(row["Receipt #"]).lower() or
            search_term in str(row["Due Date"]).lower(), axis=1)]

    if df.empty:
        st.warning("No matching records found.")
        return

    # Group by borrower
    borrowers = df["Borrower"].unique()

    for borrower in borrowers:
        with st.expander(f"💳 {borrower}"):
            df_b = df[df["Borrower"] == borrower].copy()
            df_b.reset_index(drop=True, inplace=True)

            running_balance = 0.0
            updates = []

            for i, row in df_b.iterrows():
                due = row["Due Date"]
                amount = float(str(row["Amount"]).replace("$", "").replace(",", ""))
                status = row["Status"]
                receipt = row["Receipt #"]

                col1, col2, col3, col4 = st.columns([2, 1.5, 1.5, 2])

                with col1:
                    st.markdown(f"**Due:** {due}")

                with col2:
                    st.markdown(f"**Amount:** ${amount:.2f}")

                with col3:
                    paid = st.checkbox("Paid", value=(status == "Paid"), key=f"{borrower}_{i}")
                with col4:
                    new_receipt = st.text_input("Receipt #", value=receipt, key=f"{borrower}_{i}_receipt")

                # Rule: must have receipt # to mark as paid
                new_status = "Paid" if paid and new_receipt.strip() else "Unpaid"

                if paid and not new_receipt.strip():
                    st.warning("Enter a receipt number to mark this as Paid.")

                if new_status != status or new_receipt != receipt:
                    updates.append((i, new_status, new_receipt))

                if new_status == "Unpaid":
                    running_balance += amount

            st.markdown(f"**Remaining Balance:** ${running_balance:.2f}")

            if updates:
                if st.button(f"💾 Save Changes for {borrower}"):
                    for idx, new_status, new_receipt in updates:
                        row_num = df_b.index[idx] + 2
                        sheet.update_cell(row_num, 4, new_status)
                        sheet.update_cell(row_num, 5, new_receipt)
                    st.success("Updates saved.")

