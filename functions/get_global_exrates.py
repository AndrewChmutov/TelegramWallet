import exrates
import constants
from functions.inline_keyboard import inline_keyboard_builder
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup

def get_global_exrates(amount: float, base = 'USD'):
    rates = exrates.get_exchange_rates(base)

    # loop through currencies and initialize keyboard
    response = f'**{amount} {base}** is:\n\n```'
    for currency in rates:
        formatted_float = '{:.2f}'.format(float(amount) * currency[1])
        response += '\n' + currency[0] + '  ' + formatted_float

    # inline keyboard
    button_currencies = [
        InlineKeyboardButton(cur + ('⭐️' if cur == base else ''), callback_data='g_prim' + cur ) 
        for cur in constants.currencies
    ]
    
    # creating keyboard
    markup = InlineKeyboardMarkup(inline_keyboard_builder(button_currencies, 3, False))

    return response + '\n```', markup