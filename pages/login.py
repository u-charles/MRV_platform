# pages/login.py
import streamlit as st
from db.database import SessionLocal, init_db
from db import crud
from passlib.hash import bcrypt

init_db()

def show_login():
    st.header("Login")
    db = SessionLocal()
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login"):
        if not email:
            st.error("Enter an email.")
            return
        user = crud.get_user(db, email)
        if not user:
            st.info("No account found. Please register on the Register page.")
        else:
            # verify password using passlib bcrypt
            if bcrypt.verify(password, user.password_hash):
                st.success(f"Welcome back, {user.name or user.email}!")
                st.session_state["user_email"] = user.email
                st.session_state["user_id"] = user.id
            else:
                st.error("Incorrect password. Please try again.")
    db.close()
