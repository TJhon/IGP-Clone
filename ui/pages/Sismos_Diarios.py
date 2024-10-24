import streamlit as st, datetime
from igp import SismoDataDownloader
from igp.utils import alert_string
from components.sidebar import sidebar

st.set_page_config("Sismos Diarios")

st.title("Reportes de Sismos Por Fecha")


when = st.date_input(
    "Escoja la Fecha",
    format="DD-MM-YYYY",
    max_value=datetime.datetime.now(),
)
when1 = when - datetime.timedelta(days=1)
when = when.strftime("%Y-%m-%d")


with st.spinner("Loading"):
    data = SismoDataDownloader(
        fecha_inicio=when1.strftime("%Y-%m-%d"),
        fecha_fin=when,
        tipo_catalogo="Instrumental",
    ).descargar_datos()

    data["alert"] = data["mag_m"].apply(alert_string)
    data = data.query("fecha == @when")

# st.write(data)
st.header(f"Total: {len(data)}")
if len(data) < 1:
    st.warning("No hay datos para la fecha seleccionada")
    st.stop()


with st.spinner("Cargando Mapa"):

    st.map(
        data,
        latitude="lat",
        longitude="long",
        size="prof_km",
        color="alert",
        zoom=4,
    )

sidebar()
