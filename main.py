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
        parse_mode=telegram.ParseMode.MARKDOWN_V2
    )


def help_command(update: telegram.Update, context: CallbackContext):
    response = open('commands/help.txt', 'r').read()
    update.message.reply_text(response)



# fallback
def cancel():
    return telegram.ext.ConversationHandler.END


def build_num_keyboard(specifier: str):
    buttons = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'del', '0', '.', 'Enter']
    inline_buttons = [InlineKeyboardButton(text=button, callback_data=specifier + button) for button in buttons]

    keyboard = inline_keyboard_builder(inline_buttons, columns=3)
    return keyboard


def handle_num_keyboard(amount: str, data: str) -> str:
    # if there already exists point, no possibility to add another one
    if data == '.' and amount.count('.') == 1:
        return amount
    
    # if the amount is empty
    if not amount and data not in ['del', '.', 'Enter']:
        amount += data
    # if not
    elif amount and data not in ['del', 'Enter']:
        amount += data

    # pop the last number
    if amount and data == 'del':
        amount = amount[:-1]

    return amount


def handle_num_keyboard_g_rates(update: telegram.Update, context: CallbackContext):
    data = update.callback_query.data
    
    amount: str
    text = update.callback_query.message.text.split('\n')

    if len(text) < 2:
        amount = ''
    else:
        amount = text[1]
    
    amount_new = handle_num_keyboard(amount, data[len('gex---'):])

    text = text[0] + '\n' + amount_new
    markup = InlineKeyboardMarkup(build_num_keyboard(data[:len('gex---')]))

    # if edit message and not change message,
    # then the error raises
    if amount_new == amount:
        return

    context.bot.edit_message_text(
        text=text, 
        chat_id=update.callback_query.message.chat.id,
        message_id=update.callback_query.message.message_id,
        reply_markup=markup
    )


def exchange_keyboard_builder(specifier: str):
    base = ''
    # inline keyboard
    button_currencies = [
        InlineKeyboardButton(cur + ('⭐️' if cur == base else ''), callback_data=specifier + cur ) 
        for cur in constants.currencies
    ]
    
    # creating keyboard
    markup = InlineKeyboardMarkup(inline_keyboard_builder(button_currencies, 3, False))

    return markup

# Handle the result of the choice in the main menu
def menu_message_handler(update: telegram.Update, context: CallbackContext):
    text = update.message.text
    # possible results
    match text:
        case 'Exchange rates':
            # amount = get_amount()
            # text, markup = get_info_exchange_rates()
        
            # text = '*Rates\.* Enter amount:\n'

            # markup = InlineKeyboardMarkup(build_num_keyboard('gex'))
            text = '*Global rates\.* Choose currency:'
            markup = exchange_keyboard_builder('g_rates')

            context.bot.send_message(
                text=text, 
                chat_id=update.message.chat.id, 
                parse_mode=telegram.ParseMode.MARKDOWN_V2,
                reply_markup=markup
            )
            

        # case 'Balance':
        #     text = get_balance_message(update.message.chat.id)
        #     update.message.reply_text(text=text, parse_mode=telegram.ParseMode.MARKDOWN)

            

def inline_keyboard_builder(buttons: list[InlineKeyboardButton], columns = 3, least_down = True):
    # selecting the amount of rows in keyboard
    rows = (len(buttons) / columns).__ceil__()
    keyboard = [[] for _ in range(rows)]

    # keys assignment
    
    # case when not all sells in the keyboard are filled
    # if least_down, then smaller amount of buttons will 
    # be in the last row
    if least_down:
        for idx, cur in enumerate(buttons):
            keyboard[idx // columns].append(cur)
    else:
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


def get_info_exchange_rates(amount: float, base = 'USD'):
    rates = exrates.get_exchange_rates(base)

    # loop through currencies and initialize keyboard
    response = f'**{amount} {base}** is:\n\n```'
    for currency in rates:
        formatted_float = '{:.2f}'.format(float(amount) * currency[1])
        response += '\n' + currency[0] + '  ' + formatted_float

    # inline keyboard
    button_currencies = [
        InlineKeyboardButton(cur + ('⭐️' if cur == base else ''), callback_data='g_prim' + cur ) 
        for cur in constants.currencies
    ]
    
    # creating keyboard
    markup = InlineKeyboardMarkup(inline_keyboard_builder(button_currencies, 3, False))

    # context.bot.send_message(
    #     text=response + '\n```', 
    #     chat_id=update.message.chat.id, 
    #     parse_mode=telegram.ParseMode.MARKDOWN_V2,
    #     reply_markup=markup
    # )
    return response + '\n```', markup


def edit_exchange_rates(update: telegram.Update, context: CallbackContext):
    base = update.callback_query.data
    text = update.callback_query.message.text
    amount = float(text[:text.index(' ')])


    # excluding prefix 'g_prim'
    base = base[6:]

    # getting changes
    text, markup = get_info_exchange_rates(amount, base)
    context.bot.edit_message_text(
        text,
        chat_id=update.callback_query.message.chat.id,
        message_id=update.callback_query.message.message_id,
        parse_mode=telegram.ParseMode.MARKDOWN,
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


def get_balance_message(user_id: str):
    balance = users.get_balance(user_id)
    response = 'You current balance:\n```\n'

    for currency, amount in zip(constants.currencies, balance):
        response += f'{currency}:  {amount}\n'

    return response + '\n```'

def callback_handler(update: telegram.Update, context: CallbackContext):
    data = update.callback_query.data

    if 'g_rates' in data:
        text = '**Rates.** Enter amount:\n'
        markup = InlineKeyboardMarkup(build_num_keyboard('gex' + data[len('g_rates'):]))

        context.bot.edit_message_text(
            text=text, 
            chat_id=update.callback_query.message.chat.id,
            message_id=update.callback_query.message.message_id,
            parse_mode=telegram.ParseMode.MARKDOWN,
            reply_markup = markup
        )
    elif 'gex' in data and 'Enter' in data:
        amount: str
        text = update.callback_query.message.text.split('\n')

        if len(text) < 2:
            amount = ''
        else:
            amount = text[1]
        
        if not amount:
            handle_num_keyboard_g_rates(update, context)
        else:
            base = data[len('gex'):(len('gex') + 3)]
            text, markup = get_info_exchange_rates(amount, base)

            context.bot.edit_message_text(
                text=text,
                chat_id=update.callback_query.message.chat.id,
                message_id=update.callback_query.message.message_id,
                parse_mode=telegram.ParseMode.MARKDOWN,
                reply_markup=markup
            )
    elif 'gex' in data:
        handle_num_keyboard_g_rates(update, context)
    elif 'g_prim':
        edit_exchange_rates(update, context)
    
    update.callback_query.answer()


# add functionality to the bot
def create_updater(token) -> telegram.ext.Updater:
    updater = telegram.ext.Updater(token)
    
    dispatcher = updater.dispatcher
    dispatcher.add_handler(telegram.ext.CommandHandler('start', start_command))
    dispatcher.add_handler(telegram.ext.CommandHandler('help', help_command))

    dispatcher.add_handler(telegram.ext.CallbackQueryHandler(callback_handler))
    dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, menu_message_handler))
    
    # main conversation
    # conversation_handler = telegram.ext.ConversationHandler(
    #     entry_points=[telegram.ext.CommandHandler('menu', menu_command)],
    #     states = {
    #         1: [telegram.ext.MessageHandler(telegram.ext.Filters.text, menu_message_handler)]
    #     },
    #     fallbacks=[telegram.ext.CommandHandler('cancel', cancel)]
    # )

    # dispatcher.add_handler(conversation_handler)
    
    # g_exchange_conversation = telegram.ext.ConversationHandler(
    #     entry_points=[telegram.ext.MessageHandler(g_exchange_rates_message)],
    #     states = {
    #         1: [telegram.ext.MessageHandler(get_amount)]
    #     },
    #     fallbacks=[telegram.ext.]
    # )

    return updater


# main body
if __name__ == '__main__':
    updater = create_updater(TOKEN)

    updater.start_polling()
    updater.idle()