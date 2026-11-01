import questionary
import random

from services.payment_service import complete_payment, create_pending_order, get_pending_orders
from services.currency_exchange_service import convert_currency, get_available_currencies

def convert_currency_command(amount):
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

def complete_pending_payment(account, delivery, order_id):
    card_number = questionary.text("Enter your card number: ").unsafe_ask()
    expiry = questionary.text("Enter card expiry (DD/YY): ").unsafe_ask()
    cvv = questionary.password("Enter CVV: ").unsafe_ask()

    card_details = {
                'card_number': card_number,
                'expiry': expiry,
                'cvv': cvv
    }

    return complete_payment(account, delivery, card_details, order_id, pending=True)


def complete_payment_command(account, delivery, guest_mode=False):
    print("Enter card details to proceed")
    card_number = questionary.text("Enter your card number: ").unsafe_ask()
    expiry = questionary.text("Enter card expiry (DD/YY): ").unsafe_ask()
    cvv = questionary.password("Enter CVV: ").unsafe_ask()

    card_details = {
            'card_number': card_number,
            'expiry': expiry,
            'cvv': cvv
    }
              

    order_id = create_pending_order(account)
    complete_payment(account, delivery, card_details, order_id)