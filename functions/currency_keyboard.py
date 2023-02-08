from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from functions.inline_keyboard import inline_keyboard_builder
import constants

def currency_keyboard_builder(specifier: str):
    base = ''
    # inline keyboard
    button_currencies = [
        InlineKeyboardButton(cur + ('⭐️' if cur == base else ''), callback_data=specifier + cur ) 
        for cur in constants.currencies
    ]
    
    # creating keyboard
    markup = InlineKeyboardMarkup(inline_keyboard_builder(button_currencies, 3, False))

    return markup