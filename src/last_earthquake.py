import requests
import re, json


def last_report():

    headers = {
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
    }

    response = requests.get("https://ultimosismo.igp.gob.pe/", headers=headers)

    pattern = r"window\.lastEarthquake = `(.+?)`;"

    script_content = response.text

    match = re.search(pattern, script_content)

    last_earthquake_json = {}
    if match:
        last_earthquake_json = match.group(1)
        last_earthquake_json = json.loads(last_earthquake_json)
    return last_earthquake_json


# print(last_report())
