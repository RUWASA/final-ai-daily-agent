# ui/app.py
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Daily Study Plan Agent",
    page_icon="📚",
    layout="wide"
)

# Add a sidebar logo (optional)
logo_path = Path(__file__).parent / "assets" / "logo.png"
if logo_path.exists():
    st.sidebar.image(str(logo_path), width=64)

st.sidebar.title("Navigation")
st.sidebar.radio(
    "Choose a page",
    ("Dashboard", "Add Task", "View Tasks", "Schedule", "Summary", "Study Planner"),
    index=0,
    key="nav"
)

# Use streamlit's multipage by importing pages from 'pages' package
# Streamlit will show pages automatically if placed under ./pages. We emulate that by navigation.
page = st.session_state.nav

if page == "Dashboard":
    from pages import _1_Dashboard as page_module
elif page == "Add Task":
    from pages import _2_Add_Task as page_module
elif page == "View Tasks":
    from pages import _3_View_Tasks as page_module
elif page == "Schedule":
    from pages import _4_Schedule as page_module
elif page == "Summary":
    from pages import _5_Summary as page_module
elif page == "Study Planner":
    from pages import _6_Study_Planner as page_module

page_module.app()
