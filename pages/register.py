# pages/register.py
import streamlit as st
from db.database import SessionLocal, init_db
from db import crud
from passlib.hash import bcrypt

init_db()

def show_register():
    st.header("Register")
    db = SessionLocal()
    email = st.text_input("Email", key="reg_email")
    name = st.text_input("Full name", key="reg_name")
    password = st.text_input("Password", type="password", key="reg_password")
    if st.button("Register"):
        if not email or not password or not name:
            st.error("Please provide name, email and password.")
            return
        existing = crud.get_user(db, email)
        if existing:
            st.warning("Account already exists. Please go to Login.")
        else:
            hashed = bcrypt.hash(password)
            crud.create_user(db, email=email, password_hash=hashed, name=name)
            st.success("Registration complete. Please go to Login.")
    db.close()
