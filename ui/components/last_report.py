import streamlit as st, pandas as pd
from datetime import datetime

# Cadena de fecha y hora
fecha_hora_str = "2024-10-23T13:20:34.000Z"


def last_report_view(values):
    fecha_hora = datetime.strptime(values["fecha_hora"], "%Y-%m-%dT%H:%M:%S.%fZ")
    fecha = fecha_hora.strftime("%Y-%m-%d")
    hora = fecha_hora.strftime("%H:%M:%S")
    st.header(f"Ultimo Reporte: `{fecha}` `{hora}`")
    referencia = values["referencia"]
    try:
        ref, region = referencia.split("-")
        st.markdown(
            f"Referencia: {ref} - <strong>{region}</strong>", unsafe_allow_html=True
        )

    except:
        st.write(f"Referencia: {referencia}")

    values["latitud"] = float(values["latitud"])
    values["longitud"] = float(values["longitud"])

    # color_alert = alert_string(values["magnitud"])

    col1, col2, col3 = st.columns(3)

    col2.metric("Profundidad", str(values["profundidad"]) + " Km")
    col3.metric("Latitud", values["latitud"])
    # col3.metric("Hora", hora)
    col3.metric("Longitud", values["longitud"])

    col2.metric("Magnitud", str(values["magnitud"]) + " M")
    alerta = values["alert"]
    col1.markdown(
        f"""
    <span style="width:50px; height:50px;  border-radius:50%; background-color: {alerta}; display:inline-block;"></span>
    """,
        unsafe_allow_html=True,
    )
    values_df = {}

    for key in list(values.keys()):
        values_df[key] = [values[key]]

    last_report = pd.DataFrame(values_df)

    st.map(
        last_report.reset_index(),
        latitude="latitud",
        longitude="longitud",
        size=4000,
        color=alerta,
        zoom=7,
    )
