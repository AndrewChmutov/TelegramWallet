from telegram import InlineKeyboardButton
from functions.inline_keyboard import inline_keyboard_builder

def num_keyboard_builder(specifier: str):
    buttons = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'del', '0', '.', 'Enter']
    inline_buttons = [InlineKeyboardButton(text=button, callback_data=specifier + button) for button in buttons]

    keyboard = inline_keyboard_builder(inline_buttons, columns=3)
    return keyboard