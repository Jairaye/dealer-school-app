import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st

def load_sheet_client():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    if "gcp_service_account" in st.secrets:
        # ✅ You’re in Streamlit Cloud
        creds_dict = dict(st.secrets["gcp_service_account"])
    else:
        # ✅ You’re running locally
        creds_path = os.path.expanduser("~/.gcp_keys/dealer_school.json")
        with open(creds_path) as f:
            creds_dict = json.load(f)

    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    return gspread.authorize(creds)