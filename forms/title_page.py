# forms/title_page.py

import streamlit as st

def render():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        st.markdown("<h2 style='text-align: center;'>🔒 Admin Login</h2>", unsafe_allow_html=True)
        pwd = st.text_input("Enter password", type="password")
        if st.button("Login"):
            if pwd == st.secrets["auth_password"]:
                st.session_state["authenticated"] = True
                st.success("Access granted ✅")
                st.rerun()
            else:
                st.error("Incorrect password 🚫")
        return

    # --- Background + Title ---
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;600&display=swap');

        .title-container {
            background-image: url("https://tse2.mm.bing.net/th/id/OIP.VDyT7Uh39euIMuuf3OKXvAHaEL?rs=1&pid=ImgDetMain&o=7&rm=3");
            background-size: cover;
            background-position: center;
            height: 400px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 10px;
            margin-bottom: 20px;
        }

        .title-text {
            font-family: 'Poppins', sans-serif;
            font-size: 48px;
            font-weight: 600;
            color: white;
            text-shadow: 2px 2px 4px #000;
            text-align: center;
            width: 100%;
        }
        </style>

        <div class="title-container">
            <div class="title-text">🎓 Vegas Casino Dealer Academy</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --- Welcome Message ---
    st.markdown(
        """
        <h3 style='text-align: center;'>Welcome to the Admin Dashboard</h3>
        <p style='text-align: center;'>Use the sidebar to navigate between enrollment, payments, assessments, and more.</p>
        """,
        unsafe_allow_html=True
    )
