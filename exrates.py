import json
import constants



def get_exchange_rates(base: str):
    if base not in constants.currencies:
        raise BaseException().add_note('BaseNotFound')
    
    with open('exrates.json', 'r') as exrates:
        exrates_specific_base = json.load(exrates)[base]

    return exrates_specific_base