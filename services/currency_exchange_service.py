
import requests


def get_available_currencies(default_currencies=True, excluded_currency=''):
    if default_currencies:
        available_currencies = ['USD', 'GBP', 'EUR', 'CAD', 'JPY']

        return list(filter(lambda x: x != excluded_currency, available_currencies))
    
    url = "https://api.frankfurter.dev/v2/currencies"

    currencies = requests.get(url)

    currencies.raise_for_status()
    currencies = currencies.json()

    available_currencies = []

    for currency in currencies:
        available_currencies.append(currency['iso_code'])

    return list(filter(lambda x: x != excluded_currency, available_currencies))



def get_currency_symbol(chosen_currency):
    url = f"https://api.frankfurter.dev/v2/currency/{chosen_currency}"
    
    symbol = requests.get(url)
    symbol.raise_for_status()
    symbol = symbol.json().get('symbol')

    return symbol

def calculate_exchange_rate(base_currency, chosen_currency):
    url = f"https://api.frankfurter.dev/v2/rates?base={base_currency}&quotes={chosen_currency}"

    exchange_rate = requests.get(url)
    exchange_rate.raise_for_status()
    exchange_rate = exchange_rate.json()[0].get('rate')

    return float(f'{exchange_rate:.2f}')

# print(f"1 GBP to EUR is {get_currency_symbol('eur')}{calculate_exchange_rate('gbp', 'eur')}")

available_currencies = get_available_currencies()

def check_currency_exists(currency): # USD
    return currency.upper() in available_currencies

def get_currency_value(original_c, new_c, amount):
    if original_c == new_c:
        return amount
    # exchange_rate = get_ex
    # in_usd = exchange_rates[original_c] * amount
    # to_new_c = (1 / exchange_rates[new_c]) * in_usd

    o_exchange_rate = calculate_exchange_rate(original_c, 'usd')
    # print(o_exchange_rate)
    n_exchange_rate = calculate_exchange_rate('usd', new_c)
    in_usd = o_exchange_rate * amount
    to_new_c = (1 / n_exchange_rate) * in_usd
    return to_new_c

def convert_currency(original_c, new_c, amount):
    if validate_range(original_c, amount):
        symbol = get_currency_symbol(new_c)
        value = get_currency_value(original_c, new_c, amount)
        return f'{symbol}{value:.2f}'
    else:
        return False

def validate_range(original_c, amount):
    exist = check_currency_exists(original_c)
    pounds = get_currency_value(original_c, "GBP", amount)
    return exist and 10 < pounds < 1000

# print(available_currencies)

# print(convert_currency('GBP', 'USD', 57.50))

