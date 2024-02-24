import requests
import re, json


def last_report():

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://ultimosismo.igp.gob.pe/inicio",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Upgrade-Insecure-Requests": "1",
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
