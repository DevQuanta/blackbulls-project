
exchange_rates = {
    'USD': 1.00, #I.E. 1 Pound is 1.13 Dollars
    'EUR': 1.15,
    'CAD': 0.70,
    'GBP': 1.32,
    'JPY': 0.0063,
}

symbols = {
    'USD': '$',
    'GBP': '£',
    'EUR': '€',
    'CAD': '$',
    'JPY': '¥',
}


def check_currency_exists(currency): # USD
    return currency.upper() in exchange_rates

def get_currency_value(original_c, new_c, amount):
    if original_c == new_c:
        return amount
    in_usd = exchange_rates[original_c] * amount
    to_new_c = (1 / exchange_rates[new_c]) * in_usd
    return to_new_c

def convert_currency(original_c, new_c, amount):
    if validate_range(original_c, amount):
        # print('valid amount')
        symbol = symbols[new_c]
        value = get_currency_value(original_c, new_c, amount)
        return f'{symbol}{value:.2f}'
    else:
        return False

def validate_range(original_c, amount):
    pounds = get_currency_value(original_c, "GBP", amount)
    print(f'in pounds, the value is {pounds}')
    exist = check_currency_exists(original_c)
    return exist and 10 < pounds < 1000

print(convert_currency('GBP', 'USD', 57.50))

