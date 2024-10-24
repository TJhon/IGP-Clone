import requests, time, pandas as pd, streamlit as st, pytz
from io import BytesIO


from datetime import datetime, timedelta
from typing_extensions import Literal

date_format = "%d-%m-%Y"
today = datetime.now().strftime(date_format)


def alert_string(value):
    if value < 4.5:
        return "#009900"
    elif 4.5 <= value < 6:
        return "#ffdd00"
    else:
        return "#e20000"


def peru_time(value):
    value = str(value)
    time_utc = datetime.strptime(value, "%d/%m/%Y %H:%M:%S")
    time_utc = pytz.utc.localize(time_utc)
    zone = pytz.timezone("America/Lima")
    now = time_utc.astimezone(zone)
    return now


def new_format_date(value: str):
    when = datetime.strptime(value, date_format)
    target = when.strftime("%Y-%m-%d")
    return target


class IGPData:
    def __init__(
        self,
        date=(today, today),
        lat=(-25.701, -1.396),
        lon=(-87.382, -65.634),
        magn=(1, 9),
        prof_km=(0, 900),
        type_method: Literal["instrumental", "historico"] = "instrumental",
    ):
        self.__prefix__ = "https://ultimosismo.igp.gob.pe/datos-sismicos-xls"

        str_date, end_date = date
        default_begin = str_date

        str_date = datetime.strptime(str_date, date_format)
        str_date = str_date - timedelta(days=2)
        str_date = str_date.strftime(date_format)

        end_date = datetime.strptime(end_date, date_format)
        end_date = end_date + timedelta(days=1)
        end_date = end_date.strftime(date_format)

        self.date = [default_begin, end_date]

        lat_y_min, lat_y_max = lat
        lon_x_min, lon_x_max = lon
        method_int = 1
        min_magn, max_magn = magn
        prof_km_min, prof_km_max = prof_km

        if type_method == "instrumental":
            method_int = 2

        url_values = [
            self.__prefix__,
            str_date,
            end_date,
            lat_y_min,
            lat_y_max,
            lon_x_min,
            lon_x_max,
            method_int,
            min_magn,
            max_magn,
            prof_km_min,
            prof_km_max,
        ]
        self.url = "/".join(map(str, url_values))

        self.__colnames__ = [
            "utc_date",
            "utc_time",
            "latitude",
            "longitude",
            "depth_km",
            "magnitude_m",
        ]

    def download_data(self):
        begin = time.time()
        response = requests.get(self.url).content
        excel_data = BytesIO(response)
        data = pd.read_excel(excel_data, names=self.__colnames__, engine="openpyxl")
        data["alert"] = data["magnitude_m"].apply(alert_string)

        data["utc"] = data["utc_date"] + " " + data["utc_time"]
        data["utm5"] = pd.to_datetime(data["utc"].apply(peru_time))

        dates = list(map(new_format_date, self.date))

        begin_date = pd.Timestamp(dates[0], tz="America/Lima")
        end_date = pd.Timestamp(dates[1], tz="America/Lima")

        data = data[(data["utm5"] >= begin_date) & (data["utm5"] < end_date)]
        data = data.reset_index()

        data["depth_m"] = data["depth_km"] * 50

        self.data = data

        local_data = "./data/local.csv"
        data.to_csv(local_data, index=False)

        end = time.time()
        print(end - begin)
        return self
