# app.py
import streamlit as st
from db.database import init_db
from pages import login, register, emissions_input, view_results

# Initialize DB (creates tables)
init_db()

st.set_page_config(page_title="EduMRV", layout="wide")
st.title("EduMRV — Institutional MRV (Scopes 1 | 2 | 3)")

menu = st.sidebar.selectbox("Navigation", ["Login", "Register", "Enter Emissions", "View Records"])

if menu == "Login":
    login.show_login()
elif menu == "Register":
    register.show_register()
elif menu == "Enter Emissions":
    emissions_input.show_input()
elif menu == "View Records":
    view_results.show_results()
