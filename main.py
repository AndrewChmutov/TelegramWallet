import telegram
import telegram.ext
from telegram import ReplyKeyboardMarkup
from telegram import KeyboardButton
from telegram.ext import CallbackContext

# custom library
import users
import exrates

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


# Main menu of actions
def menu_command(update: telegram.Update, context: CallbackContext):
    exrates = KeyboardButton('Exchange rates')
    balance = KeyboardButton('Balance')
    markup_reply = ReplyKeyboardMarkup([[exrates], [balance]], resize_keyboard=True)
    context.bot.send_message(update.message.chat.id, 'Enter action:', reply_markup=markup_reply)

    return 1


# fallback
def cancel():
    return telegram.ext.ConversationHandler.END


# Handle the result of the choice in the main menu
def menu_message_handler(update: telegram.Update, context: CallbackContext):
    update.message.reply_text(update.message.text.upper())
    text = update.message.text
    # possible results
    match text:
        case 'Exchange rates':
            print_exchange_rates(update, context)
            

def print_exchange_rates(update: telegram.Update, context):
    base = 'USD'
    rates = exrates.get_exchange_rates(base)
    # loop through currencies and initialize keyboard
    response = f'*1 {base}* is:\n\n```'
    for currency in rates:
        formatted_float = '{:.2f}'.format(currency[1])
        response += '\n' + formatted_float + ' ' * (6 - len(formatted_float) % 7) + currency[0]
    print(response)
    update.message.reply_text(response + '\n```', parse_mode=telegram.ParseMode.MARKDOWN_V2)



def error_handler(update: telegram.Update, context: CallbackContext):
    print(f'Update: {update}, \n\nerror: {context.error}')


# add functionality to the bot
def create_updater(token) -> telegram.ext.Updater:
    updater = telegram.ext.Updater(token)
    
    dispatcher = updater.dispatcher
    dispatcher.add_handler(telegram.ext.CommandHandler('start', start_command))
    dispatcher.add_handler(telegram.ext.CommandHandler('help', help_command))

    # main conversation
    conversation_handler = telegram.ext.ConversationHandler(
        entry_points=[telegram.ext.CommandHandler('menu', menu_command)],
        states = {
            1: [telegram.ext.MessageHandler(telegram.ext.Filters.text, menu_message_handler)]
        },
        fallbacks=[telegram.ext.CommandHandler('cancel', cancel)]
    )

    dispatcher.add_handler(conversation_handler)

    return updater


# main body
if __name__ == '__main__':
    updater = create_updater(TOKEN)

    updater.start_polling()
    updater.idle()