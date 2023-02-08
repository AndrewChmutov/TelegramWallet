from telegram import Update
from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup
from telegram import ParseMode
from telegram.ext import CallbackContext

import users

def start_handler(update: Update, context: CallbackContext):
    # add user
    users.add_user(
        update.message.chat.id,
        update.message.chat.first_name + ' ' + update.message.chat.last_name, 
        update.message.chat.username
    )

    # response
    response = open('commands/start.txt', 'r').read()

    # main menu of actions
    wallet = KeyboardButton('My wallet')
    exrates = KeyboardButton('Exchange rates')
    settings = KeyboardButton('Settings')
    adm_tools = KeyboardButton('Admin tools')

    markup_reply = ReplyKeyboardMarkup(
        [[wallet, exrates], 
        [settings, adm_tools]], 
        resize_keyboard=True
    )
    
    context.bot.send_message(
        update.message.chat.id, 
        text=response, 
        reply_markup=markup_reply,
        parse_mode=ParseMode.MARKDOWN_V2
    )
