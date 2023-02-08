from telegram import Update, ParseMode
from telegram import InlineKeyboardMarkup
from telegram.ext import CallbackContext

from builder import SuperBuilder
from handler import SuperHandler
import users
import constants

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
        elif 'Top-up' in data or ('topam' in data and 'back' in data):
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
        elif 'Enter' in data and 'topam' in data:
            base = data[len('wallet:topam:'):len('wallet:topam:') + 3]
            amount: str
            text = update.callback_query.message.text.split('\n')

            if len(text) < 3:
                amount = ''
            else:
                amount = text[2]

            if not amount:
                SuperHandler.top_up_num(update, context)

            answer = users.top_up(
                str(update.callback_query.message.chat.id),
                base,
                float(amount)
            )

            match answer:
                case 0:
                    text = '*Transaction successfully finished:*\n'
                    text += f'{amount} {base} are topped up.'
                case 1:
                    text = '*Transaction cancelled:*\n'
                    text += 'You achieved the limit of specific currency (over 10^6)'
            
            text += '\n\nCurrent balance:```'
            balance = users.get_balance(str(update.callback_query.message.chat.id))
    
            for currency, amount in zip(constants.currencies, balance):
                text += '\n' + currency + ': ' + '{:.2f}'.format(amount)
            
            text += '```'

            context.bot.edit_message_text(
                text=text,
                chat_id=update.callback_query.message.chat_id,
                message_id=update.callback_query.message.message_id,
                parse_mode=ParseMode.MARKDOWN
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