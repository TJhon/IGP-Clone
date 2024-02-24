import streamlit as st, datetime, geopandas as gpd
from shapely.geometry import Point
from src.data import IGPData, today

from componets.sidebar import sidebar

st.set_page_config("Reporte Detallado")

today_f = today.replace("-", "/")
st.title("Reporte Detallado")

region = gpd.read_file(
    "./data/departamentos/DEPARTAMENTOS_inei_geogpsperu_suyopomalia.shp"
)
cols_region = ["NOMBDEP", "geometry"]
# st.write(region[cols_region])
region = region[cols_region]
regiones = region["NOMBDEP"].tolist()


# with st.expander("Filtros"):

col1, col2 = st.columns(2)

with col1:

    st.header("Filtros")
    st.subheader("Por Regiones")
    regions_filter = st.multiselect("Seleccione las regiones", regiones, default=None)
    st.subheader("Por Fecha")
    dcol1, dcol2 = st.columns(2)
    begin = dcol1.date_input(
        "Fecha Inicial",
        format="DD-MM-YYYY",
        value=datetime.datetime.now() - datetime.timedelta(days=30),
    )
    begin = begin.strftime("%d-%m-%Y")

    end = dcol2.date_input(
        "Fecha Final",
        format="DD-MM-YYYY",
        max_value=datetime.datetime.now(),
    )
    end = end.strftime("%d-%m-%Y")

    st.subheader("Por Magnitud")

    mcol1, mcol2 = st.columns(2)
    min_m = mcol1.slider("Magnitud mínima", min_value=1, max_value=8, value=1)
    max_m = mcol2.slider("Magnitud ", min_value=1, max_value=9, value=9)

    st.subheader("Por Profundidad")
    mcol1, mcol2 = st.columns(2)
    min_p = mcol1.slider("Profundidad mínima", min_value=0, max_value=9, value=0)
    max_p = mcol2.slider("Profundidad maxima", min_value=0, max_value=900, value=900)


with col2:
    with st.spinner("Loading"):
        today_data = IGPData(
            date=(begin, end), magn=(min_m, max_m), prof_km=(min_p, max_p)
        ).download_data()

    data = today_data.data

    geometry = [
        Point(lon, lat) for lon, lat in zip(data["longitude"], data["latitude"])
    ]
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
        # st.write(data)

    st.header(f"Total: {len(data)}")

    with st.spinner("Cargando Mapa"):

        @st.cache_data
        def convert_df(df):
            return df.to_csv(index=False).encode("utf-8")

        csv = convert_df(data)

        # st.dataframe(data)

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

sidebar()
