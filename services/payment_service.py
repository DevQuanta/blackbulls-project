from services.location_service import validate_postcode
import random
from services.account_service import update_account
from environment import LAET_COUNTRY_CODE, LAET_POSTCODE
from services.currency_service import price_in_another_currency
from services.location_service import calculate_distance

def calculate_delivery_fees(distance):
    delivery_fees = 15
    if distance > 3000:
        delivery_fees = 100
    elif distance > 2000 and distance <= 3000:
        delivery_fees = 75
    elif distance > 1000 and distance <= 2000:
        delivery_fees = 50
    return delivery_fees
        
    
    
def complete_payment(account, delivery, guest_mode=False):

    card_number = input("Enter your card number: ")
    expiry = input("Enter card expiry (DD/YY): ")
    cvv = input("Enter CVV: ")

    order_id = f"TX_{random.randint(1029384, 4382284038)}"

    order = {
        'order_id': order_id,
        'items': account["basket"]["items"],
        'delivery_details': {
            'postcode': delivery["postcode"]
        },
        'total_price': account["basket"]["total_price"],
        'payment_status': 'completed'
    }



    account["orders"].append(order)
    account["basket"]["items"] = {}
    account["basket"]["total_price"] = 0
    account["basket"]["tax"] = 0

    if not guest_mode:
        update_account(account)

    print("Payment completed.")
    


def get_address(details):
    return details["properties"]["address_line1"]

def get_lat_long(details):
    return {
        'lon': details["properties"]["lon"],
        'lat': details["properties"]["lat"]
    }

def checkout_basket(account):
    country_code = input("Enter your country code (US): ")
    address = input("Enter your address")
    delivery_postcode = input("Enter your postcode: ")

    delivery_details = validate_postcode(delivery_postcode, country_code)
    laet_details = validate_postcode(LAET_POSTCODE, LAET_COUNTRY_CODE)

    laet_coords = get_lat_long(laet_details)
    delivery_coords = get_lat_long(delivery_details)

    print(f'LAET coords: {laet_coords}')
    print(f'Delivery coords: {delivery_coords}')

    delivery_address = get_address(delivery_details)
    
    distance = calculate_distance(laet_coords, delivery_coords)
    print(distance)

    tax = random.randint(1,100)
    delivery_fees = calculate_delivery_fees(distance)
    total_price = account['basket']['total_price']
    total_price += tax
    total_price += delivery_fees

    print(f"The total price in GBP is £{total_price}")
    convert = input("Would you like to convert the final price to another currency? Y/n ")

    if convert.lower() == "y":
        total_price = price_in_another_currency(total_price)

    delivery_details = {
        'address': address,
        'postcode': delivery_postcode,
    }

    complete_payment(account, delivery_details)
