from datetime import datetime
import pytz


tz = pytz.timezone("America/Lima")


current_time = datetime.now(tz)


ymd = current_time.strftime("%Y-%m-%d")
dmy = current_time.strftime("%d-%m-%Y")
