from telegram import Update
from telegram.ext import CallbackContext
from telegram import InlineKeyboardMarkup
from builder import SuperBuilder


def handle_num_keyboard_g_rates(update: Update, context: CallbackContext):
    data = update.callback_query.data
    
    amount: str
    text = update.callback_query.message.text.split('\n')

    if len(text) < 2:
        amount = ''
    else:
        amount = text[1]
    
    amount_new = SuperBuilder.use_num_keyboard_g_exrates(amount, data[len('gex---'):])

    text = text[0] + '\n' + amount_new
    markup = InlineKeyboardMarkup(SuperBuilder.num_keyboard(data[:len('gex---')]))

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