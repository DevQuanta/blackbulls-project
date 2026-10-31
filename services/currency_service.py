from currency_exchange import convert_currency, get_available_currencies

def price_in_another_currency(amount):
    default_currencies = get_available_currencies(excluded_currency='GBP')

    for idx, currency in enumerate(default_currencies):
            print(f'{idx + 1}. {currency}')
    print(f"{len(default_currencies) + 1}. Other currency")

    new_currency_idx = int(input("What currency do you want it to be converted into? ")) - 1

    if new_currency_idx == len(default_currencies):
        available_currencies = get_available_currencies(default_currencies=False, excluded_currency='GBP')

        for idx, currency in enumerate(available_currencies):
            print(f'{idx + 1}. {currency}')

        new_currency_idx = int(input("What currency do you want it to be converted into? ")) - 1
        new_currency = available_currencies[new_currency_idx]
    else:
        new_currency = default_currencies[new_currency_idx]

    total_price = convert_currency("GBP", new_currency, amount)

    return total_price
