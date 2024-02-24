import streamlit as st, pandas as pd

from src.last_earthquake import last_report
from src.data import alert_string

values = last_report()


def last_report_view():

    st.header(f"Ultimo Reporte: `{values['fecha_local']}`")

    st.write(f"Referencia: {values['referencia']}")
    color_alert = alert_string(values["magnitud"])

    col1, col2, col3 = st.columns(3)

    col2.metric("Profundidad", str(values["profundidad"]) + " Km")
    col2.metric("Latitud", values["latitud"])
    col3.metric("Hora", values["hora_local"])
    col3.metric("Longitud", values["longitud"])

    col1.metric("Magnitud", str(values["magnitud"]) + " M")
    col1.markdown(
        f"""
    <span style="width:50px; height:50px; background-color:{color_alert}; border-radius:50%; display:inline-block;"></span>
    """,
        unsafe_allow_html=True,
    )
    values_df = {}

    for key in list(values.keys()):
        values_df[key] = [values[key]]

    last_report = pd.DataFrame(values_df)
    last_report["alert"] = last_report["magnitud"].apply(alert_string)

    st.map(
        last_report.reset_index(),
        latitude="latitud",
        longitude="longitud",
        size=4000,
        # color="#3198c4",
        color="alert",
        zoom=7,
    )
