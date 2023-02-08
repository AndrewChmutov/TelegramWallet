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
    exrates = KeyboardButton('Exchange rates')
    balance = KeyboardButton('Balance')
    markup_reply = ReplyKeyboardMarkup([[exrates], [balance]], resize_keyboard=True)
    context.bot.send_message(
        update.message.chat.id, 
        text=response, 
        reply_markup=markup_reply,
        parse_mode=ParseMode.MARKDOWN_V2
    )
