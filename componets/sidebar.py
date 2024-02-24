import streamlit as st


def sidebar():
    with st.sidebar:
        st.button("Refresh", type="primary", use_container_width=True)
