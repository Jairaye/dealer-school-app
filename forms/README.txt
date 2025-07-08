Dealer School Streamlit App - README
=====================================

Overview:
---------
This Streamlit app is designed for use by a single administrator to handle:
- Student Enrollment
- Payment Agreements & Tracking
- Initial & Final Skill Assessments
- Metrics Dashboard (planned)

Project Structure:
------------------
dealer_school_app/
├── app.py
├── credentials.json              # Service account key file (DO NOT SHARE)
├── forms/
│   ├── enrollment_form.py
│   ├── payment_form.py
│   ├── payment_tracker.py
│   └── assessment_form.py
├── data/
│   └── (reserved for any future offline data)
├── utils/
│   └── (helper functions if needed)
└── README.txt                    # <- This file

Google Sheet Integration:
-------------------------
- Sheet Name: Dealer_academy_records
- Must have 3 tabs:
  - "Enrollment"       → for student intake records
  - "Payments"         → for agreement meta-data
  - "Payment Tracking" → auto-generated payment plan, status, receipts
  - "Assessments"      → for skill evaluation (Initial/Final)

Sheet Naming Rules:
-------------------
- Sheet tab names must use spaces (NOT underscores).
- Headers MUST include:
  - "Student ID" in Enrollment
  - "Borrower", "Due Date", "Amount", "Status", "Receipt #" in Payment Tracking

Student ID Format:
------------------
Auto-generated during enrollment:
  VCD-YY-INITIALS-XXXX
    - VCD = Vegas Casino Dealer
    - YY = two-digit year (e.g., 25)
    - INITIALS = currently hardcoded to JR
    - XXXX = random 4-digit number
Example: VCD-25-JR-3842

Submission Notes:
-----------------
- Enrollment form will only submit if all required fields are filled.
- Enrollment appends to Google Sheet tab "Enrollment".
- Payment form allows selection of frequency & due date.
- Payment plan auto-calculates and submits to "Payment Tracking".
- Payment Tracker allows updating status to "Paid" ONLY after entering a receipt number.
- Assessments require Student ID to be pre-existing in "Enrollment".

Deployment Notes:
-----------------
- App runs locally or via Streamlit Cloud
- If deployed via Streamlit Cloud:
  - credentials.json must be stored in secrets manager (NOT in repo)
  - User will need access to the linked Google Sheet

Pending Features:
-----------------
- Metrics Dashboard (quarterly/yearly breakdowns)
- Print/export reports
- Auto-email confirmations (future)

Created by: J.R.
For: Vegas Casino Dealer Academy
