import streamlit as st, datetime, geopandas as gpd
from shapely.geometry import Point
from igp import SismoDataDownloader
from igp.utils import alert_string

from components.sidebar import sidebar, filter_date_utm

st.set_page_config("Reporte Detallado")


st.title("Reporte Detallado")

region = gpd.read_file(
    "./data/departamentos/DEPARTAMENTOS_inei_geogpsperu_suyopomalia.shp"
)
cols_region = ["NOMBDEP", "geometry"]
# st.write(region[cols_region])
region = region[cols_region]
regiones = region["NOMBDEP"].tolist()


# with st.expander("Filtros"):
date_format = "%Y-%m-%d"
col1, col2 = st.columns(2)

with col1:

    st.header("Filtros")
    # st.subheader("Por Regiones")
    regions_filter = st.multiselect("Seleccione las regiones", regiones, default=None)
    # st.subheader("Por Fecha")
    dcol1, dcol2 = st.columns(2)
    begin = dcol1.date_input(
        "Fecha Inicial",
        format="DD-MM-YYYY",
        value=datetime.datetime.now() - datetime.timedelta(days=30),
    )
    begin = begin.strftime(date_format)

    end = dcol2.date_input(
        "Fecha Final",
        format="DD-MM-YYYY",
        max_value=datetime.datetime.now(),
    )
    end = end.strftime(date_format)

    # st.subheader("Por Magnitud")

    mcol1, mcol2 = st.columns(2)
    min_m, max_m = st.select_slider(
        "Magnitud", options=list(range(1, 10)), value=(1, 9)
    )

    # st.subheader("Por Profundidad")
    min_p, max_p = st.select_slider(
        "Profundidad", options=list(range(1, 901)), value=(1, 900)
    )


with col2:
    with st.spinner("Loading"):

        data = SismoDataDownloader(
            fecha_inicio=begin,
            fecha_fin=end,
            minima_magnitud=min_m,
            maxima_magnitud=max_m,
            minima_profundidad=min_p,
            maxima_profundidad=max_p,
            tipo_catalogo="Instrumental",
        ).descargar_datos()

        if len(data) < 1:
            st.warning("No hay datos")
            st.stop()

        data["alert"] = data["mag_m"].apply(alert_string)
        data = filter_date_utm(data, begin, end)

    geometry = [Point(lon, lat) for lon, lat in zip(data["long"], data["lat"])]
    if len(regions_filter) > 0:
        # st.write(regions_filter)
        data_gpd = gpd.GeoDataFrame(data, geometry=geometry, crs="EPSG:4326")
        regions_df = region.query("NOMBDEP in @regions_filter")
        data = (
            gpd.sjoin(data_gpd, regions_df, how="right", predicate="within")
            .drop(columns=["geometry"])
            .dropna()
            .reset_index()
        )
        if len(data) < 1:
            st.warning("No hay datos")
            st.stop()
        # st.write(data)

    st.header(f"Total: {len(data)}")

    with st.spinner("Cargando Mapa"):

        st.map(
            data,
            latitude="lat",
            longitude="long",
            size="mag_m",
            color="alert",
            zoom=3.8,
        )


@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode("utf-8")


csv = convert_df(data)

st.download_button(
    "Descargar datos como csv",
    data=csv,
    file_name=f"igp_eartquake_{begin}_{end}.csv",
    mime="text/csv",
)

sidebar()
