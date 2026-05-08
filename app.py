# Main entry point (UI navigation)
import streamlit as st
from ui_pages.teacher import teacher_page
from ui_pages.reviewer import reviewer_page
from ui_pages.admin import admin_page
from ui_pages.parents import parent_page

# ---------------------------
# APP CONFIG
# ---------------------------
st.set_page_config(page_title="Document Workflow System", layout="wide")

st.title("📄 Document Workflow System")

# ---------------------------
# ROLE SELECTION
# ---------------------------
st.sidebar.title("Select Role")

role = st.sidebar.radio(
    "Choose your role:",
    ["Teacher", "Reviewer","Parent","Admin"]
)
st.sidebar.divider()

# ---------------------------
# ROLE ROUTING
# ---------------------------
if role == "Teacher":
    teacher_page()

elif role == "Reviewer":
    reviewer_page()

elif role == "Admin":
    admin_page()

elif role == "Parent":
    parent_page()
# ---------------------------
# FOOTER / INFO
# ---------------------------
st.sidebar.divider()
st.sidebar.info(
    """
    Workflow:
    Draft → Review → Approve → Send
    
    Features:
    - Version Control
    - Rejection Loop
    - Send Failure Handling
    """
)