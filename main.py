import time
from igp.last_earthquake import SismoDataDownloader, pd

begin = time.time() 

downloader = SismoDataDownloader(fecha_inicio="1960-01-01", fecha_fin="2024-10-19")

end_api_igp = time.time()

print(f"time api igp: {end_api_igp - begin }\n")


raw_csv = (
    "https://raw.githubusercontent.com/TJhon/IGP-Clone/refs/heads/refactor/data/all.csv"
)

data = pd.read_csv(raw_csv)

end_gh_api = time.time()


print(f"time api gh: {end_gh_api- end_api_igp }\n")
