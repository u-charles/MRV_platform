# pages/emissions_input.py
import streamlit as st
import pandas as pd
from db.database import SessionLocal
from db import crud
from calculator import get_factors, calculate_bulk, get_scope

def show_input():
    st.header("Enter emissions quantities (multiple categories)")

    if "user_email" not in st.session_state:
        st.info("Please log in first.")
        return

    db = SessionLocal()
    user = crud.get_user(db, st.session_state["user_email"])
    if not user:
        st.error("User not found in DB.")
        db.close()
        return

    factors = get_factors()
    keys = list(factors.keys())

    st.markdown("Enter quantities for any categories that apply — leave 0 for those that don't.")
    cols = st.columns(2)

    inputs = {}
    for i, k in enumerate(keys):
        label = k.replace("_", " ").title()
        unit = ""  # unit could be shown from CSV if desired
        col = cols[i % 2]
        inputs[k] = col.number_input(f"{label} ({unit})", min_value=0.0, format="%.3f", key=f"inp_{k}")

    if st.button("Calculate & Save All"):
        details, total = calculate_bulk(inputs)
        if not details:
            st.info("No values entered.")
            db.close()
            return

        # Save each non-zero entry to DB with scope from mapping
        saved = 0
        for k, v in inputs.items():
            if v and float(v) > 0:
                emission = calculate_bulk({k: v})[0][k]
                scope = get_scope(k)
                crud.create_emission_record(db, user.id, k, float(v), float(emission), scope=scope)
                saved += 1

        st.success(f"Saved {saved} records. Total emissions: {total} kg CO₂e")
        st.table(pd.DataFrame([{"activity": k, "emission_kg": e} for k, e in details.items()]))

    db.close()
