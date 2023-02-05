import telegram
import telegram.ext
from telegram.ext import CallbackContext

# custom library
import users

# token of the bot. For individual use, you should enter yous
TOKEN = open('token.txt', mode='r').read()


# handling commands and conversations
def start_command(update: telegram.Update, context: CallbackContext):
    # add user
    users.add_user(update.message.chat_id)

    # response
    response = open('commands/start.txt', 'r').read()
    update.message.reply_text(response, parse_mode=telegram.ParseMode.MARKDOWN)


def help_command(update: telegram.Update, context: CallbackContext):
    response = open('commands/help.txt', 'r').read()
    update.message.reply_text(response)


def error_handler(update: telegram.Update, context: CallbackContext):
    print(f'Update: {update}, \n\nerror: {context.error}')


# add functionality to the bot
def create_updater(token) -> telegram.ext.Updater:
    updater = telegram.ext.Updater(token)
    
    dispatcher = updater.dispatcher
    dispatcher.add_handler(telegram.ext.CommandHandler('start', start_command))
    dispatcher.add_handler(telegram.ext.CommandHandler('help', help_command))

    return updater


# main body
if __name__ == '__main__':
    updater = create_updater(TOKEN)

    updater.start_polling()
    updater.idle()