from telegram import Update
from telegram.ext import CallbackContext

def error_handler(update: Update, context: CallbackContext):
    print(f'Update: {update}, \n\nerror: {context.error}')