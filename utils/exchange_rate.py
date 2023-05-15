import requests


def get_exrate(currency_code_name) -> float:
    # credit to https://tw.rter.info/howto_currencyapi.php
    # thanks a lot
    try:
        resp = requests.get("https://tw.rter.info/capi.php")
        currency = resp.json()
        return currency[currency_code_name]["Exrate"]
    except Exception:
        return 30.4
