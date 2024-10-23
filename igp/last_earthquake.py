import requests
import pandas as pd, time
from datetime import datetime, timedelta
from io import BytesIO


def last():

    data = requests.get("https://ultimosismo.igp.gob.pe/api/ultimo-sismo")
    return data.json()


class SismoDataDownloader:
    def __init__(
        self,
        tipo_catalogo="Instrumental",
        fecha_inicio="2024-01-01",
        fecha_fin="2024-10-19",
        minima_magnitud=1,
        maxima_magnitud=9,
        minima_profundidad=0,
        maxima_profundidad=900,
        latitud_norte=-1.396,
        latitud_sur=-25.701,
        longitud_este=-65.624,
        longitud_oeste=-87.382,
    ):
        self.base_url = (
            "https://ultimosismo.igp.gob.pe/api/ultimo-sismo/descargar-datos"
        )

        self.params = {
            "tipoCatalogo": tipo_catalogo,
            "fechaInicio": fecha_inicio,
            "fechaFin": fecha_fin,
            "minimaMagnitud": minima_magnitud,
            "maximaMagnitud": maxima_magnitud,
            "minimaProfundidad": minima_profundidad,
            "maximaProfundidad": maxima_profundidad,
            "latitudNorte": latitud_norte,
            "latitudSur": latitud_sur,
            "longitudEste": longitud_este,
            "longitudOeste": longitud_oeste,
        }

    @staticmethod
    def convertir_utc_a_peru(fecha, hora):

        if len(hora) > 8:
            hora = hora[:8]
        datetime_str = f"{fecha} {hora}"

        dt_utc = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")

        dt_peru = dt_utc - timedelta(hours=5)

        return dt_peru.strftime("%Y-%m-%d"), dt_peru.strftime("%H:%M:%S")

    def descargar_datos(self, save_csv=False, csv_filename=None) -> pd.DataFrame:
        if save_csv:
            if csv_filename is None:
                raise ("You need a csv filename")
        if csv_filename is not None:
            save_csv = True

        # print(self.base_url)

        response = requests.get(self.base_url, params=self.params)

        excel_data = BytesIO(response.content)

        data = pd.read_excel(excel_data)

        base_columns = ["fecha_utc", "hora_utc", "lat", "long", "prof_km", "mag_m"]

        if self.params["tipoCatalogo"].lower() == "historico":
            base_columns = base_columns + ["mag_ms", "mag_mw"]
        data.columns = base_columns
        data["type"] = self.params["tipoCatalogo"].lower()
        # fecha UTC     hora UTC  latitud (º)  longitud (º)  profundidad (km)  magnitud (mb)  magnitud (Ms)  magnitud (Mw)

        data["fecha"], data["hora"] = zip(
            *data.apply(
                lambda row: self.convertir_utc_a_peru(
                    row["fecha_utc"], row["hora_utc"]
                ),
                axis=1,
            )
        )
        data.drop(columns=["fecha_utc", "hora_utc"], inplace=True)
        self.data = data
        if save_csv:
            data.to_csv(csv_filename, index=False)
            print(f"Archivo {csv_filename} guardado como CSV.")
        return data


# Uso de la clase
# downloader = SismoDataDownloader(fecha_inicio="1960-01-01", fecha_fin="2024-10-23")
# data = downloader.descargar_datos(
#     csv_filename="./data/instrumental/archive/23-10-2024.csv"
# )
# data.to_csv("./data/instrumental/instrumental_data.csv", index=False)
# print(data)


# inst = pd.read_csv("./data/instrumental/instrumental_data.csv")
# hist = pd.read_csv("./data/historical/historical_data.csv")

# data = pd.concat([hist, inst], ignore_index=True)
# data.to_csv("./data/all_data.csv", index=False)
