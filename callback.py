from telegram import Update, ParseMode
from telegram import InlineKeyboardMarkup
from telegram.ext import CallbackContext

from builder import SuperBuilder
from handler import SuperHandler

def callback_handler(update: Update, context: CallbackContext):
    data = update.callback_query.data
    print(data)
    # EXCHANGE RATES
    if 'gex'in data:
        if 'back' in data and 'begin' not in data:
            text = '*Global rates.* Choose currency:'
            markup = SuperBuilder.currency_keyboard('gex:begin:')

            context.bot.edit_message_text(
                text=text, 
                chat_id=update.callback_query.message.chat.id, 
                message_id=update.callback_query.message.message_id,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=markup
            )
        elif 'begin' in data:
            # Here the user enters specific amount
            # with virtual keyboard. It is used to
            # dictate the rules of input
            base =  data[len('gex:begin:'):]
            text = f'*Global rates {base}.* Enter amount:\n'
            markup = InlineKeyboardMarkup(SuperBuilder.num_keyboard('gex:' + base))

            context.bot.edit_message_text(
                text=text, 
                chat_id=update.callback_query.message.chat.id,
                message_id=update.callback_query.message.message_id,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup = markup
            )
        elif 'Enter' in data:
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
                base = data[len('gex:'):(len('gex:') + 3)]
                text, markup = SuperBuilder.get_global_exrates(amount, base)

                context.bot.edit_message_text(
                    text=text,
                    chat_id=update.callback_query.message.chat.id,
                    message_id=update.callback_query.message.message_id,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=markup
                )
        elif 'g_prim' in data:
            SuperHandler.edit_g_exrates(update, context)
        else:
            SuperHandler.num_keyboard_g_exrates(update, context)

    elif 'wallet' in data:
        if 'topcur' in data and 'back' in data:
            text, markup = SuperBuilder.wallet_menu(str(update.callback_query.message.chat.id))

            context.bot.edit_message_text(
                text=text,
                chat_id=update.callback_query.message.chat.id,
                message_id=update.callback_query.message.message_id,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=markup
            )
        elif 'Top-up' in data:
            text = '*WALLET\TOP-UP*\nChoose the currency for top-up'
            markup = SuperBuilder.currency_keyboard('wallet:topcur:')

            context.bot.edit_message_text(
                text=text,
                chat_id=update.callback_query.message.chat_id,
                message_id=update.callback_query.message.message_id,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=markup
            )
        elif 'topcur' in data:
            base = data[len('wallet:topcur:'):len('wallet:topcur:') + 3]
            text = f'*WALLET\TOP-UP\{base}*\nEnter the desired amount:\n'
            keyboard = SuperBuilder.num_keyboard(f'wallet:topam:{base}')
            markup = InlineKeyboardMarkup(keyboard)
            
            context.bot.edit_message_text(
                text=text,
                chat_id=update.callback_query.message.chat_id,
                message_id=update.callback_query.message.message_id,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=markup
            )
        elif 'topam' in data:
            SuperHandler.top_up_num(update, context)

        elif 'back' in data:
            text, markup = SuperBuilder.wallet_menu(update.callback_query.message.chat.id)

            context.bot.edit_message_text(
                text=text,
                chat_id=update.callback_query.message.chat_id,
                message_id=update.callback_query.message.message_id,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=markup
            )

    update.callback_query.answer()