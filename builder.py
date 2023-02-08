import functions.currency_keyboard
import functions.num_keyboard
import functions.get_global_exrates
import functions.use_num_keyboard_g_exrates

class SuperBuilder:
    currency_keyboard           = functions.currency_keyboard.currency_keyboard_builder
    inline_keyboard             = functions.inline_keyboard.inline_keyboard_builder
    num_keyboard                = functions.num_keyboard.num_keyboard_builder
    get_global_exrates          = functions.get_global_exrates.get_global_exrates
    use_num_keyboard_g_exrates  = functions.use_num_keyboard_g_exrates.use_num_keyboard_g_exrates