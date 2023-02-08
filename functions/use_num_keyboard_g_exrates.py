def use_num_keyboard_g_exrates(amount: str, data: str) -> str:
    # if there already exists point, no possibility to add another one
    if data == '.' and amount.count('.') == 1:
        return amount
    
    # if the amount is empty
    if not amount and data not in ['del', '.', 'Enter']:
        amount += data
    # if not
    elif amount and data not in ['del', 'Enter']:
        amount += data

    # pop the last number
    if amount and data == 'del':
        amount = amount[:-1]

    return amount