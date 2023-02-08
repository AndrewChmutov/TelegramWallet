import handlers.start_handler
import handlers.help_handler
import handlers.error_handler
import handlers.main_menu_handler
import handlers.num_keyboard_g_exrates_handler
import handlers.edit_g_exrates_handler

from telegram.ext import CommandHandler as ch
from telegram.ext import MessageHandler as mh
import telegram.ext

class SuperHandler:
    start                   = handlers.start_handler.start_handler
    help                    = handlers.help_handler.help_handler
    error                   = handlers.error_handler.error_handler
    main_menu               = handlers.main_menu_handler.main_menu_handler
    num_keyboard_g_exrates  = handlers.num_keyboard_g_exrates_handler.handle_num_keyboard_g_rates
    edit_g_exrates          = handlers.edit_g_exrates_handler.edit_g_exrates_handler
    
    def get_handler(entity: str):
        mapping_entities = {
            'start':    (ch, SuperHandler.start),
            'help':     (ch, SuperHandler.help),
            'main_menu':(mh, SuperHandler.main_menu),
            'error':    (None, SuperHandler.error)
        }

        handler, command = mapping_entities[entity]

        if handler is ch:
            return ch(entity, command)
        elif handler is mh:
            return mh(telegram.ext.Filters.text, command)
        elif handler is None:
            return command

        return