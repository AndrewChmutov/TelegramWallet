import telegram
import telegram.ext
from telegram import ReplyKeyboardMarkup
from telegram import KeyboardButton
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram.ext import CallbackContext

# custom library
import users
import exrates
import constants

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
            

def inline_keyboard_builder(buttons: list[InlineKeyboardButton], columnts = 2):
    # selecting the amount of rows in keyboard
    rows = (len(buttons) / 2).__ceil__()
    keyboard = [[] for _ in range(rows)]

    # keys assignment
    if len(buttons) % 2 == 0:
        for idx, cur in enumerate(buttons):
            keyboard[idx // 2].append(cur)
    else:
        keyboard[0].append(buttons[0])
        
        for idx, cur in enumerate(buttons):
            if idx == 0:
                continue

            keyboard[1 + (idx - 1) // 2].append(cur)
    
    return keyboard


def print_exchange_rates(update: telegram.Update, context: CallbackContext):
    base = 'USD'
    rates = exrates.get_exchange_rates(base)

    # loop through currencies and initialize keyboard
    response = f'*1 {base}* is:\n\n```'
    for currency in rates:
        formatted_float = '{:.2f}'.format(currency[1])
        response += '\n' + formatted_float + ' ' * (6 - len(formatted_float) % 7) + currency[0]

    # inline keyboard
    button_currencies = [
        InlineKeyboardButton(cur, callback_data='prim' + cur + ('⭐️' if cur == base else '')) 
        for cur in constants.currencies
    ]
    
    markup = InlineKeyboardMarkup(inline_keyboard_builder(button_currencies))
    context.bot.send_message(
        text=response + '\n```', 
        chat_id=update.message.chat.id, 
        parse_mode=telegram.ParseMode.MARKDOWN_V2,
        reply_markup=markup
    )




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