from igp import SismoDataDownloader
from time_now import ymd, dmy


instrumental = SismoDataDownloader(
    fecha_inicio="1960-01-01",
    fecha_fin=ymd,
    tipo_catalogo="Historico",
).descargar_datos(csv_filename=f"../data/historical/archive/{dmy}.csv")

instrumental.to_csv("../data/instrumental/instrumental_data.csv", index=False)

print("all_done")
