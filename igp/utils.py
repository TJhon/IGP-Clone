def alert_string(value):
    value = float(value)
    if value < 4.5:
        return "#009900"
    elif 4.5 <= value < 6:
        return "#ffdd00"
    else:
        return "#e20000"
