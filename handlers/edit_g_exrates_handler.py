from telegram import Update, ParseMode
from telegram.ext import CallbackContext
from builder import SuperBuilder

def edit_g_exrates_handler(update: Update, context: CallbackContext):
    base = update.callback_query.data
    text = update.callback_query.message.text
    amount = float(text[:text.index(' ')])


    # excluding prefix 'g_prim'
    base = base[6:]

    # getting changes
    text, markup = SuperBuilder.get_global_exrates(amount, base)
    context.bot.edit_message_text(
        text,
        chat_id=update.callback_query.message.chat.id,
        message_id=update.callback_query.message.message_id,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=markup
    )
    update.callback_query.answer()