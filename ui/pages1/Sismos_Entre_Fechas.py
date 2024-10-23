import streamlit as st, datetime
from src.data import IGPData, today

st.set_page_config("Reporte: Sismos Entre Fechas")

today_f = today.replace("-", "/")
st.title("Reportes de Sismos Por Fecha")

col1, col2 = st.columns(2)
begin = col1.date_input(
    "Fecha Inicial",
    format="DD-MM-YYYY",
    value=datetime.datetime.now() - datetime.timedelta(days=7),
)
begin = begin.strftime("%d-%m-%Y")

end = col2.date_input(
    "Fecha Final",
    format="DD-MM-YYYY",
    max_value=datetime.datetime.now(),
)
end = end.strftime("%d-%m-%Y")


with st.spinner("Loading"):
    today_data = IGPData(date=(begin, end)).download_data()

data = today_data.data


st.header(f"Total: {len(data)}")

with st.spinner("Cargando Mapa"):

    @st.cache_data
    def convert_df(df):
        return df.to_csv(index=False).encode("utf-8")

    csv = convert_df(data)

    st.map(
        data,
        latitude="latitude",
        longitude="longitude",
        size="depth_m",
        color="alert",
        zoom=3.8,
    )

    st.download_button(
        "Download data as CSV",
        data=csv,
        file_name=f"igp_eartquake_{begin}_{end}.csv",
        mime="text/csv",
    )


from componets.sidebar import sidebar

sidebar()
