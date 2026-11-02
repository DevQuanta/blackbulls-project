import questionary

from rich.console import Console
from services.payment_service import complete_payment, create_pending_order, save_delivery_details
from services.currency_exchange_service import convert_currency, get_available_currencies

console = Console()

def convert_currency_command(amount):
    default_currencies = get_available_currencies(excluded_currency='GBP')

    choices = [{
         'name': name,
         'value': idx
    } for idx, name in enumerate(default_currencies)]

    choices.append({
         'name': 'Other currency',
         'value': len(default_currencies)
    })

    choice = questionary.select("Choose currency to pay in", choices=choices).unsafe_ask()

    if choice == len(default_currencies):
        available_currencies = get_available_currencies(default_currencies=False, excluded_currency='GBP')

        all_choices = [{
                 'name': name,
                 'value': idx
            } for idx, name in enumerate(available_currencies)]

        
        choice = questionary.select("Choose currency to pay in", choices=all_choices).unsafe_ask()

        new_currency = available_currencies[choice]
    else:
        new_currency = default_currencies[choice]

    (symbol, total_price) = convert_currency("GBP", new_currency, amount)
    console.print(f"The new price is [bright_cyan]{symbol}{total_price}[/bright_cyan]")

    return (symbol, total_price)

def complete_pending_payment(account, order_id):
    card_number = questionary.text("Enter your card number: ").unsafe_ask()
    expiry = questionary.text("Enter card expiry (DD/YY): ").unsafe_ask()
    cvv = questionary.password("Enter CVV: ").unsafe_ask()

    card_details = {
        'card_number': card_number,
        'expiry': expiry,
        'cvv': cvv
    }

    return complete_payment(account, card_details, order_id, pending=True)


def complete_payment_command(account, total_price, symbol, delivery, guest_mode=False):
    order_id = create_pending_order(account, symbol, total_price, guest_mode)
    if not guest_mode:
        save_delivery_details(account, order_id, delivery)

    card_number = questionary.text("Enter your card number: ").unsafe_ask()
    expiry = questionary.text("Enter card expiry (DD/YY): ").unsafe_ask()
    cvv = questionary.password("Enter CVV: ").unsafe_ask()

    card_details = {
        'card_number': card_number,
        'expiry': expiry,
        'cvv': cvv
    }

    complete_payment(account, card_details, order_id, guest_mode = guest_mode)

    console.print("[green]Order has been confirmed![/green]")

    return True