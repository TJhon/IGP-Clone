def alert_string(value):
    value = float(value)
    if value < 4.5:
        return "#009900"
    elif 4.5 <= value < 6:
        return "#ffdd00"
    else:
        return "#e20000"


from datetime import datetime
import pytz


tz = pytz.timezone("America/Lima")


current_time = datetime.now(tz)


ymd = current_time.strftime("%Y-%m-%d")
dmy = current_time.strftime("%d-%m-%Y")
