import streamlit as st
st.set_page_config(page_title="Dealer Academy", layout="wide")  # ✅ KEEP THIS ONE
st.write("Secrets available:", dict(st.secrets))

from forms import title_page, enrollment_form, payment_form, payment_tracker, assessment_form

# 🔥 DELETE THIS DUPLICATE LINE:
# st.set_page_config(page_title="Dealer Academy", layout="wide")

# Global CSS injection
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;600&display=swap');

    html, body, div, span, input, label, textarea, select {
        font-family: 'Poppins', sans-serif !important;
    }

    [data-testid="stAppViewContainer"] {
        background-color: #e0f0ff !important;
    }

    [data-testid="stHeader"] {
        background: none;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("📋 Navigation")
page = st.sidebar.radio("Go to:", [
    "Home",
    "Enrollment Form",
    "Payment Agreement",
    "Track Payments",
    "Assessments"
])

# Routing
if page == "Home":
    title_page.render()
elif page == "Enrollment Form":
    enrollment_form.render()
elif page == "Payment Agreement":
    payment_form.render()
elif page == "Track Payments":
    payment_tracker.render()
elif page == "Assessments":
    assessment_form.render()

