import json
import requests
import constants

def refresh():
    truncated = {}
    for currency in constants.currencies:
        truncated[currency] = []
        for cur in constants.currencies:
            if currency == cur:
                continue
            url = f'https://open.er-api.com/v6/latest/{currency}'
            truncated[currency].append((cur, requests.get(url).json()['rates'][cur]))

    with open('exrates.json', 'w') as exrates:
        json.dump(truncated, exrates)

def get_exchange_rates(base: str):
    if base not in constants.currencies:
        raise BaseException().add_note('BaseNotFound')
    
    with open('exrates.json', 'r') as exrates:
        exrates_specific_base = json.load(exrates)[base]

    return exrates_specific_base