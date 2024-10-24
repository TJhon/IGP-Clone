# intenta con la fecha actual (mensual), y reemplaza el anterior archivo
from igp import SismoDataDownloader
from time_now import ymd, dmy

historical = SismoDataDownloader(
    fecha_inicio="1471-01-01",
    fecha_fin="1959-12-31",
    tipo_catalogo="Historico",
).descargar_datos(csv_filename=f"./data/historical/archive/{dmy}.csv")

historical.to_csv("./data/historical/historical_data.csv", index=False)

print("all_done")
