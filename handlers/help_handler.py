from telegram import Update
from telegram.ext import CallbackContext

def help_handler(update: Update, context: CallbackContext):
    response = open('commands/help.txt', 'r').read()
    update.message.reply_text(response)

    update.callback_query.answer()