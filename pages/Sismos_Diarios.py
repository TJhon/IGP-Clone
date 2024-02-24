import streamlit as st, datetime
from src.data import IGPData, today


st.set_page_config("Sismos Diarios")


today_f = today.replace("-", "/")
st.title("Reportes de Sismos Por Fecha")


when = st.date_input(
    "Escoja la Fecha",
    format="DD-MM-YYYY",
    max_value=datetime.datetime.now(),
)
when = when.strftime("%d-%m-%Y")

with st.spinner("Loading"):
    today_data = IGPData(date=(when, when)).download_data()

data = today_data.data


st.header(f"Total: {len(data)}")


with st.spinner("Cargando Mapa"):

    st.map(
        data,
        latitude="latitude",
        longitude="longitude",
        size="depth_m",
        color="alert",
        zoom=3.8,
    )
