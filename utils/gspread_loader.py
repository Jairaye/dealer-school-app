import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def load_sheet_client():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds_path = os.path.expanduser("~/.gcp_keys/dealer_school.json")
    with open(creds_path) as f:
        creds_dict = json.load(f)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    return gspread.authorize(creds)