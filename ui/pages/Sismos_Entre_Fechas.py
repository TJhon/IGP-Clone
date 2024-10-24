import streamlit as st, datetime
from igp import SismoDataDownloader
from igp.utils import alert_string
from components.sidebar import sidebar


st.set_page_config("Reporte: Sismos Entre Fechas")


st.title("Reportes de Sismos Por Fecha")

now = datetime.datetime.now()

col1, col2 = st.columns(2)
begin = col1.date_input(
    "Fecha Inicial",
    format="DD-MM-YYYY",
    value=now - datetime.timedelta(days=7),
)
begin = begin.strftime("%Y-%m-%d")

end = col2.date_input(
    "Fecha Final",
    format="DD-MM-YYYY",
    max_value=now,
)
end = end.strftime("%Y-%m-%d")


with st.spinner("Loading"):
    data = SismoDataDownloader(
        fecha_inicio=begin,
        fecha_fin=end,
        tipo_catalogo="Instrumental",
    ).descargar_datos()
    data["alert"] = data["mag_m"].apply(alert_string)


st.header(f"Total: {len(data)}")

with st.spinner("Cargando Mapa"):

    @st.cache_data
    def convert_df(df):
        return df.to_csv(index=False).encode("utf-8")

    csv = convert_df(data)

    st.map(
        data,
        latitude="lat",
        longitude="long",
        size="prof_km",
        color="alert",
        zoom=3.8,
    )

    st.download_button(
        "Download data as CSV",
        data=csv,
        file_name=f"igp_eartquake_{begin}_{end}.csv",
        mime="text/csv",
    )
sidebar()
