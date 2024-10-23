from components import last_report, sidebar

# from src.last_earthquake import last_report as lr
from igp import SismoDataDownloader, last
import streamlit as st


st.set_page_config(page_title="IGP: Ultimo Reporte")
sidebar.sidebar()


last_report.last_report_view(last())
