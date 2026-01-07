import streamlit as st

def kpi(label, value):
    st.markdown(
        f"""
        <div style='padding:20px;border-radius:10px;
        border:1px solid #ccc;background-color:#f9f9f9;'>
            <h4>{label}</h4>
            <h2>{value}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )
