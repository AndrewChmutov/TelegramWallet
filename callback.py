from telegram import Update, ParseMode
from telegram import InlineKeyboardMarkup
from telegram.ext import CallbackContext

from builder import SuperBuilder
from handler import SuperHandler

def callback_handler(update: Update, context: CallbackContext):
    data = update.callback_query.data

    # EXCHANGE RATES
    if 'g_rates' in data:
        # Here the user enters specific amount
        # with virtual keyboard. It is used to
        # dictate the rules of input
        text = '**Rates.** Enter amount:\n'
        markup = InlineKeyboardMarkup(SuperBuilder.num_keyboard('gex' + data[len('g_rates'):]))

        context.bot.edit_message_text(
            text=text, 
            chat_id=update.callback_query.message.chat.id,
            message_id=update.callback_query.message.message_id,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup = markup
        )
    elif 'gex' in data and 'Enter' in data:
        # If the input is complete

        # Also check if there is a number at least
        amount: str
        text = update.callback_query.message.text.split('\n')

        if len(text) < 2:
            amount = ''
        else:
            amount = text[1]
        
        if not amount:
            SuperHandler.num_keyboard_g_exrates(update, context)
        else:
            # build final keyboard
            base = data[len('gex'):(len('gex') + 3)]
            text, markup = SuperBuilder.get_global_exrates(amount, base)

            context.bot.edit_message_text(
                text=text,
                chat_id=update.callback_query.message.chat.id,
                message_id=update.callback_query.message.message_id,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=markup
            )
    elif 'gex' in data:
        SuperHandler.num_keyboard_g_exrates(update, context)
    elif 'g_prim':
        SuperHandler.edit_g_exrates(update, context)
    
    update.callback_query.answer()