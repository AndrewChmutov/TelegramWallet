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
    update.message.reply_text(response, parse_mode=telegram.ParseMode.MARKDOWN_V2)


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
            text, markup = get_info_exchange_rates()
            
            context.bot.send_message(
                text=text, 
                chat_id=update.message.chat.id, 
                parse_mode=telegram.ParseMode.MARKDOWN_V2,
                reply_markup=markup
            )
            

def inline_keyboard_builder(buttons: list[InlineKeyboardButton], columns = 3):
    # selecting the amount of rows in keyboard
    rows = (len(buttons) / columns).__ceil__()
    keyboard = [[] for _ in range(rows)]

    # keys assignment
    
    # where to start second row assignmens
    cont_from = len(buttons) % columns

    if cont_from == 0:
        for idx, cur in enumerate(buttons):
            keyboard[idx // columns].append(cur)
    else:
        # fill the first row
        for i in range(cont_from):
            keyboard[0].append(buttons[i])
        
        # fill other rows
        for idx, cur in enumerate(buttons):
            if idx < cont_from:
                continue

            keyboard[1 + (idx - cont_from) // columns].append(cur)

    return keyboard


def get_info_exchange_rates(base = 'USD'):
    rates = exrates.get_exchange_rates(base)

    # loop through currencies and initialize keyboard
    response = f'*1 {base}* is:\n\n```'
    for currency in rates:
        formatted_float = '{:.2f}'.format(currency[1])
        response += '\n' + formatted_float + ' ' * (6 - len(formatted_float) % 7) + currency[0]

    # inline keyboard
    button_currencies = [
        InlineKeyboardButton(cur + ('⭐️' if cur == base else ''), callback_data='prim' + cur ) 
        for cur in constants.currencies
    ]
    
    # creating keyboard
    markup = InlineKeyboardMarkup(inline_keyboard_builder(button_currencies, 3))

    # context.bot.send_message(
    #     text=response + '\n```', 
    #     chat_id=update.message.chat.id, 
    #     parse_mode=telegram.ParseMode.MARKDOWN_V2,
    #     reply_markup=markup
    # )
    return response + '\n```', markup


def edit_exchange_rates(update: telegram.Update, context: CallbackContext):
    base = update.callback_query.data

    if 'prim' not in base:
        return

    # excluding prefix 'prim'
    base = base[4:]

    # getting changes
    text, markup = get_info_exchange_rates(base)
    context.bot.edit_message_text(
        text,
        chat_id=update.callback_query.message.chat.id,
        message_id=update.callback_query.message.message_id,
        parse_mode=telegram.ParseMode.MARKDOWN_V2,
        reply_markup=markup
    )
    # )
    # update.message.edit_text(
    #     text,
    #     chat_id=update.message.chat.id,
    #     message_id=update.message.message_id,
    #     parse_mode=telegram.ParseMode.MARKDOWN_V2,
    #     reply_markup=markup
    # )

    update.callback_query.answer()

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
    dispatcher.add_handler(telegram.ext.CallbackQueryHandler(edit_exchange_rates))
    return updater


# main body
if __name__ == '__main__':
    updater = create_updater(TOKEN)

    updater.start_polling()
    updater.idle()