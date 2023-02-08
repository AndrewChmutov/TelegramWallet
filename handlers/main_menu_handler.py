from telegram import Update, ParseMode
from telegram.ext import CallbackContext
from builder import SuperBuilder

# Handle the result of the choice in the main menu
def main_menu_handler(update: Update, context: CallbackContext):
    text = update.message.text
    # possible results
    match text:
        case 'Exchange rates':
            text = '**Global rates.** Choose currency:'
            markup = SuperBuilder.currency_keyboard('g_rates')

            context.bot.send_message(
                text=text, 
                chat_id=update.message.chat.id, 
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=markup
            )
        case 'My wallet':
            text, markup = SuperBuilder.wallet_keyboard(str(update.message.chat.id))

            context.bot.send_message(
                text=text,
                chat_id=update.message.chat.id,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=markup
            )