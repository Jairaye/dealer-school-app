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
        # ✅ Cloud mode
        creds_dict = dict(st.secrets["gcp_service_account"])
        creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n").strip()

        # 👇 Diagnostic block (runs only in cloud)
        print("⏎ Key Preview:")
        for i, line in enumerate(creds_dict["private_key"].split("\n")):
            print(f"{i:02d}: {len(line)} | {line}")
    else:
        # ✅ Local dev mode
        creds_path = "C:/Users/joshu/.gcp_keys/dealer_school.json"  # Your actual file path
        with open(creds_path) as f:
            creds_dict = json.load(f)

    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    return gspread.authorize(creds)