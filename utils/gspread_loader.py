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
        # ✅ Cloud mode: use Streamlit secrets
        creds_dict = dict(st.secrets["gcp_service_account"])
        creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n").strip()

        # 🧪 Optional: Diagnostic output to logs (remove once working)
        print("⏎ Key Preview:")
        for i, line in enumerate(creds_dict["private_key"].split("\n")):
            print(f"{i:02d}: {len(line)} | {line}")
    else:
        # ✅ Local mode: use .json file
        creds_path = os.path.expanduser("~/.gcp_keys/dealer_school.json")
        with open(creds_path) as f:
            creds_dict = json.load(f)

    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    return gspread.authorize(creds)