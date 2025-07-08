import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.title("Google Sheet Connection Test")

try:
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
    client = gspread.authorize(creds)

    # Only the Sheet ID from the URL
    sheet_id = "1aj5MjgdhuG-EPTrB4pMYvxrJ0T1pOJwDIZbxL4LYbPI"
    sheet = client.open_by_key(sheet_id).sheet1

    sheet.update("A1", "✅ Connected successfully from Streamlit!")
    st.success("✅ Google Sheet updated successfully.")

except Exception as e:
    st.error(f"❌ Error: {e}")
