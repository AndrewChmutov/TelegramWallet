from telegram import InlineKeyboardButton

def inline_keyboard_builder(buttons: list[InlineKeyboardButton], columns = 3, least_down = True):
    # selecting the amount of rows in keyboard
    rows = (len(buttons) / columns).__ceil__()
    keyboard = [[] for _ in range(rows)]

    # keys assignment
    
    # case when not all sells in the keyboard are filled
    # if least_down, then smaller amount of buttons will 
    # be in the last row
    if least_down:
        for idx, cur in enumerate(buttons):
            keyboard[idx // columns].append(cur)
    else:
        # where to start second row assignmens
        cont_from = len(buttons) % columns
        if cont_from == 0:
            for idx, cur in enumerate(buttons):
                keyboard[idx // columns].append(cur)
        else:
            # fill the first row
            for i in range(cont_from):
                keyboard[0].append(buttons[i])
            
            # fill other rows
            for idx, cur in enumerate(buttons):
                if idx < cont_from:
                    continue

                keyboard[1 + (idx - cont_from) // columns].append(cur)

    return keyboard