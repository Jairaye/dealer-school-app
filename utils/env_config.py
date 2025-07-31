# utils/env_config.py

import streamlit as st

def get_env_mode():
    """Detects if app is running locally or in cloud, based on secrets"""
    auth_key = st.secrets.get("auth_password", "")
    if auth_key == "your_local_test_key":
        return "local"
    elif auth_key:
        return "cloud"
    return "unknown"

def is_debug_enabled():
    """Optional sidebar toggle for debug view (only appears in local mode)"""
    mode = get_env_mode()
    if mode == "local":
        return st.sidebar.checkbox("🔍 Enable Debug Mode", value=True)
    return False

def safe_get_secret(key, default=None):
    """Failsafe secret access to prevent KeyErrors"""
    return st.secrets.get(key, default)