import questionary
from services.location_service import calculate_distance
from commands.payment_commands import complete_payment_command, convert_currency_command, complete_pending_payment
from services.payment_service import calculate_delivery_fees, get_pending_orders
import random


def checkout_basket(account):
    pending_orders = get_pending_orders(account)
    country_code = questionary.text("Enter your country code (US): ").unsafe_ask()
    address = questionary.text("Enter your address: ").unsafe_ask()
    delivery_postcode = questionary.text("Enter your postcode: ").unsafe_ask()

    delivery_details = {
            'address': address,
            'postcode': delivery_postcode,
        }
        
    if pending_orders:
        last_order = pending_orders[-1]
        option = input("Would you like to continue the last order?") == "Y"

        if option:
            print(f"order id is {last_order}")
            return complete_pending_payment(account, delivery_details, last_order)
    
    distance = calculate_distance(delivery_postcode, country_code)

    tax = random.randint(1,100)
    delivery_fees = calculate_delivery_fees(distance)
    total_price = account['basket']['total_price']
    total_price += tax
    total_price += delivery_fees

    print(f"The total price in GBP is £{total_price}")
    choices = [{'name': 'Yes', 'value': 'Y'}, {'name': 'No', 'value': 'N'}]
    convert = questionary.select("Would you like to convert the final price to another currency?", choices = choices).ask()

    if convert.lower() == "y":
        total_price = convert_currency_command(total_price)

    
    complete_payment_command(account, delivery_details)