import questionary
from services.location_service import calculate_distance
from commands.payment_commands import complete_payment_command, convert_currency_command, complete_pending_payment
from services.payment_service import calculate_delivery_fees, get_pending_orders
from services.account_service import remove_pending_order
import random
from rich.console import Console

console = Console()

def checkout_basket(account, guest_mode=False):
    if not guest_mode:
        pending_orders = get_pending_orders(account)

        if pending_orders:
            last_order = pending_orders[-1]
            choices = [{'name': 'Yes', 'value': 'Y'}, {'name': 'No', 'value': 'N'}]
            choice = questionary.select("Would you like to continue last order?", choices = choices).ask()

            if choice == "Y":
                return complete_pending_payment(account, last_order)
            else:
                remove_pending_order(account, last_order)

    
    country_code = questionary.text("Enter your country code (US): ").unsafe_ask()
    address = questionary.text("Enter your address: ").unsafe_ask()
    delivery_postcode = questionary.text("Enter your postcode: ").unsafe_ask()

    delivery_details = {
            'address': address,
            'postcode': delivery_postcode,
    }

    
    distance = calculate_distance(delivery_postcode, country_code)

    while distance is None:
        console.print("Invalid postcode entered.")
        country_code = questionary.text("Enter your country code (US): ").unsafe_ask()
        address = questionary.text("Enter your address: ").unsafe_ask()
        delivery_postcode = questionary.text("Enter your postcode: ").unsafe_ask()

        distance = calculate_distance(delivery_postcode, country_code)


    tax = random.randint(1,100)
    delivery_fees = calculate_delivery_fees(distance)
    (symbol, total_price) = ('£', account['basket']['total_price'])
    total_price += tax
    total_price += delivery_fees

    console.print(f"The total price in GBP is [bright_cyan]£{total_price}[/bright_cyan]")
    choices = [{'name': 'Yes', 'value': 'Y'}, {'name': 'No', 'value': 'N'}]
    convert = questionary.select("Would you like to convert the final price to another currency?", choices = choices).ask()

    if convert== "Y":
        (symbol, total_price) = convert_currency_command(total_price)

    print(f'guest mode in chekcout is {guest_mode}')
    complete_payment_command(account, total_price, symbol, delivery_details, guest_mode)