# pages/view_results.py
import streamlit as st
import pandas as pd
import altair as alt
from db.database import SessionLocal
from db import crud

def show_results():
    st.header("My Emission Records & Scope Summary")
    if "user_email" not in st.session_state:
        st.info("Please log in.")
        return

    db = SessionLocal()
    user = crud.get_user(db, st.session_state["user_email"])
    if not user:
        st.error("User not found.")
        db.close()
        return

    records = crud.get_user_emissions(db, user.id)
    if not records:
        st.info("No records yet.")
        db.close()
        return

    df = pd.DataFrame([{
        "Category": r.category,
        "Quantity": r.quantity,
        "Emission (kg CO₂e)": r.emission,
        "Scope": r.scope,
        "Timestamp": r.timestamp
    } for r in records])

    st.dataframe(df)

    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X("Category:N", sort=None),
        y="Emission (kg CO₂e):Q",
        color="Scope:N",
        tooltip=["Category", "Emission (kg CO₂e)", "Quantity", "Scope", "Timestamp"]
    ).properties(title="Emissions by Category")

    st.altair_chart(chart, use_container_width=True)

    totals = df.groupby("Scope")["Emission (kg CO₂e)"].sum().reset_index()
    st.write("### Totals by Scope")
    st.dataframe(totals)

    db.close()
