import telegram
import telegram.ext
import time
import threading

# custom library
from handler import SuperHandler
import callback
import exrates

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


def do_refreshes():
    while True:
        exrates.refresh()
        time.sleep(60 * 60)


# main body
if __name__ == '__main__':
    updater = create_updater(TOKEN)

    threading.Thread(target=do_refreshes).start()

    updater.start_polling()
    updater.idle()