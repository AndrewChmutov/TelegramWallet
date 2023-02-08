from telegram import Update
from telegram.ext import CallbackContext
from telegram import InlineKeyboardMarkup
from telegram import ParseMode
from builder import SuperBuilder


def top_up_num_handler(update: Update, context: CallbackContext):
    data = update.callback_query.data
    base = data[len('wallet:topam:'):len('wallet:topam:') + 3]
    
    amount: str
    text = update.callback_query.message.text.split('\n')

    if len(text) < 3:
        amount = ''
    else:
        amount = text[2]
    
    print(amount)
    amount_new = SuperBuilder.use_num_keyboard_g_exrates(amount, data[len('wallet:topam:---'):])
    print(amount_new)

    text = '*' + text[0] + '*' + '\n' + text[1] + '\n' + amount_new
    markup = InlineKeyboardMarkup(SuperBuilder.num_keyboard(data[:len('wallet:topam:---')]))

    # if edit message and not change message,
    # then the error raises
    if amount_new == amount:
        return

    context.bot.edit_message_text(
        text=text, 
        chat_id=update.callback_query.message.chat.id,
        message_id=update.callback_query.message.message_id,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=markup
    )