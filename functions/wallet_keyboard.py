import users
import constants
from functions.inline_keyboard import inline_keyboard_builder
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup

def wallet_keyboard(user_id: str):
    text = 'Your balance:\n```'

    balance = users.get_balance(user_id)
    
    for currency, amount in zip(constants.currencies, balance):
        text += '\n' + currency + ': ' + '{:.2f}'.format(amount)

    text += '```'
    text += '\n\nChoose the action:'

    captions = ['Top-up', 'Withdraw', 'Convert', 'Exchange rates']
    buttons = [InlineKeyboardButton(text=button, callback_data='wallet:' + button) for button in captions]
    buttons = inline_keyboard_builder(buttons, columns=2)
    markup = InlineKeyboardMarkup(buttons)
    
    return text, markup