from componets import last_report, sidebar
import streamlit as st

# st.write(str_date)

st.set_page_config(page_title="IGP: Ultimo Reporte")

sidebar.sidebar()


last_report.last_report_view()
