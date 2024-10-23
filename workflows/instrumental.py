from igp import SismoDataDownloader
from time_now import ymd, dmy


instrumental = SismoDataDownloader(
    fecha_inicio="1960-01-01",
    fecha_fin=ymd,
    tipo_catalogo="Instrumental",
).descargar_datos(csv_filename=f"./data/historical/archive/{dmy}.csv")

instrumental.to_csv("./data/instrumental/instrumental_data.csv", index=False)

# last date log
# actualizamos hasta que fecha estan los datos para tenerlo como referencia y no hacer el pull de todos los datos nuevamente
import pandas as pd

logs = pd.read_csv("./data/logs.csv")
logs["last"] = 0
new_last = pd.DataFrame({"date": [dmy], "last": [1]})
logs = pd.concat([new_last, logs], ignore_index=True)
logs.to_csv("./data/logs.csv", index=False)
