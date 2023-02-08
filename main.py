import telegram
import telegram.ext

# custom library
from handler import SuperHandler
import callback

# token of the bot. For individual use, you should enter yous
TOKEN = open('token.txt', mode='r').read()

# add functionality to the bot
def create_updater(token) -> telegram.ext.Updater:
    updater = telegram.ext.Updater(token)
    
    dispatcher = updater.dispatcher
    dispatcher.add_handler(SuperHandler.get_handler('start'))
    dispatcher.add_handler(SuperHandler.get_handler('help'))
    dispatcher.add_handler(SuperHandler.get_handler('main_menu'))
    dispatcher.add_error_handler(SuperHandler.error)

    # separately.
    # callbacks are handled separately from other handlers
    dispatcher.add_handler(telegram.ext.CallbackQueryHandler(callback.callback_handler))

    return updater


# main body
if __name__ == '__main__':
    updater = create_updater(TOKEN)

    updater.start_polling()
    updater.idle()