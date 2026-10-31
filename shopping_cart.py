import json
import random
from currency_exchange import convert_currency, available_currencies, get_available_currencies


products = {
     'Titos Homemade Vodka': 18.50,
     'Another Hendricks Gin': 33.50,
     'Aperol': 13.00,
     'Bumbu original': 38.50,
     'Forte Alto Pinot Grigio': 10.00,
     'Campari Bitters': 16.00,
     'Waitrose London Dry Gin': 20.25,
     'Louis Roederer Cristal': 280.00,
     'Dom Perigton Vintage': 210.00,
     'Dalmore 15 Year Old Single Malt': 111.00,
     'Star Hill Farm Whisky': 100.00,
 }

import requests
from geopy.distance import geodesic


API_KEY = "981ff34f4d5e47ff88228d0df3564c8f"
ACCOUNT_FILE = "user_account.json"
LAET_POSTCODE = 'N17 0BX'
LAET_COUNTRY_CODE = 'gb'

mapping = {}

def validate_postcode(postcode, country_code):
    address = lookup_postcode(postcode, country_code)

    if address is None:
        print("Postcode does not exist")
        return None

    return address

def calculate_distance(point1, point2):
    url = "https://api.geoapify.com/v1/geometry/operation"

    print('\nPoints:')
    print(point1, point2)

    request_body = {
        "operation": "distance",
        "point1": {
            "type": "Point",
            "coordinates": [
                point1["lon"],
                point1["lat"]
            ]
        },
        "point2": {
            "type": "Point",
            "coordinates": [
                point2["lon"],
                point2["lat"]
            ]
        },
        "params": {
            "units": "miles"
        }
    }

    response = requests.post(url, json=request_body, params = {
            "apiKey": API_KEY
    })

    response.raise_for_status()

    response = response.json()
    return float(f"{response['data']:.2f}")


def lookup_postcode(postcode, country_code):
    url = "https://api.geoapify.com/v1/postcode/search"

    """
    https://api.geoapify.com/v1/postcode/search?postcode=90210&countrycode=us&lang=en&format=geojson&geometry=point&apiKey=981ff34f4d5e47ff88228d0df3564c8f
    """

    response = requests.get(url, params = {
        "postcode": postcode,
        "countrycode": country_code.lower(),
        "format": "geojson",
        "apiKey": API_KEY
    })

    response.raise_for_status()

    response = response.json()

    # with open("country_postcode.json", "r") as f:
    #     response = json.load(f)

    normalise = lambda s: "".join(s.upper().split())

    for result in response.get("features", []):
        if (normalise(result.get("properties", "").get("postcode", ""))) == normalise(postcode) and normalise(result.get("properties").get("country_code")) == normalise(country_code):
            return result

    return None


# a = lookup_postcode("90210", "US")

def calculate_delivery_fees(distance):
    delivery_fees = 15
    if distance > 3000:
        delivery_fees = 100
    elif distance > 2000 and distance <= 3000:
        delivery_fees = 75
    elif distance > 1000 and distance <= 2000:
        delivery_fees = 50
    return delivery_fees

        
    

def guest_mode():
    option = input("Would you like to:\n1. View basket\n2. Checkout basket\n3. Add products\n4. Quit\n> ")

    account = {
            'name': 'Guest',
            'basket': {
                'items': {},
                'total_price': 0,
                'tax': 0
            },
            'orders': []
        }
    

    while option != '4':
        match option:
            case '1':
                fetch_basket(account)
            case '2':
                checkout_basket(account)
            case '3':
                browse_products(account, guest_mode = True)

        option = input("Would you like to:\n1. View basket\n2. Checkout basket\n3. Add products\n4. Quit\n> ")

def main():
    option = input("Would you like to:\n1. Sign in\n2. Create an account\n3. Continue as guest\n4. Quit\n> ")

    while option != '4':

        match option.strip():
            case '1':
                email = input("Please enter your email: ")
                password = input("Please enter your password: ")
                account = get_account(email, password)

                while not account:
                    print("Incorrect email or password. Please try again!\n")
                    email = input("Please enter your email: ")
                    password = input("Please enter your password: ")

                    account = get_account(email, password)

                print(f"Welcome back, {account['name']}!\n")

            case '2':
                account = create_account()

            case '3':
                guest_mode()

        option = input("Would you like to:\n1. View basket\n2. Checkout basket\n3. Add products\n4. View previous orders\n5. Logout\n> ")

        while option != '5':
            match option:
                case '1':
                    fetch_basket(account)
                case '2':
                    checkout_basket(account)
                case '3':
                    browse_products(account)
                case '4':
                    fetch_orders(account)
                case '5':
                    break

            option = input("Would you like to:\n1. View basket\n2. Checkout basket\n3. Add products\n4. Logout\n> ")
            

        option = input("Would you like to:\n1. View basket\n2. Checkout basket\n3. Add products\n4. View previous orders\n5. Logout\n> ")

def fetch_orders(account):
    for order in account.get('orders', {}):
            print(f'Order ID: {order["order_id"]}')
            print(f'Items ordered:')
            for name, product in order["items"].items():
                print(f"ID #{product["product_id"]} {name}")
                print(f"Quantity: {product["quantity"]}")
                print(f"Price: £{product["price"]}\n")

            print(f'Delivery Address: {order["delivery_details"]["postcode"]}')
            print(f'Price paid: £{order["total_price"]}')
            print(f'Payment status: {order["payment_status"]}')
    


def create_account():
  
    name = input("What is your name? ")
    email = input("What is your email? ")
    password = input("What is your password? ")
    repeat_password = input("Please confirm your password: ")

    while repeat_password != password:
        print("To confirm your password...you must type it out again.")
        password = input("Please input your password: ")
        repeat_password = input("Please confirm your password: ")
    
    account = {
        'name': name,
        'email': email,
        'password': repeat_password,
        'basket': {
            'items': {},
            'total_price': 0,
            'tax': 0
        },
        'orders': []
    }

    existing_accounts = get_existing_accounts()
    
    with open(ACCOUNT_FILE, "w") as account_file:
        existing_accounts[email] = account
        json.dump(existing_accounts, account_file, indent = 2)
 
    return account 

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
    

def get_existing_accounts():
    try:
        with open(ACCOUNT_FILE, "r") as account_file:
            existing_accounts = json.load(account_file)
    except:
        existing_accounts = {}

    return existing_accounts

def print_and_get_available_products(product_catalogue):
    for product_id, (name,price) in enumerate(product_catalogue.items()):
        mapping[product_id] = name

        print(f'ID: {product_id + 1}')
        print(f'Name: {name}')
        print(f'Price: £{price}\n')

    return mapping

def fetch_basket(account):
    for name, product in account.get('basket', {}).get('items', {}).items():
        print(f'ID: {product["product_id"]}')
        print(f'Name: {name}')
        print(f'Price: £{product["price"]}')
        print(f'Quantity: {product["quantity"]}\n')

    print(f'-----\nTOTAL PRICE: £{account['basket']['total_price']}\n-----')

def get_account(email, password):
    existing_accounts = get_existing_accounts()
    return existing_accounts.get(email, None) if existing_accounts.get(email, None).get('password', None) == password else None

def browse_products(account, choice="Y", guest_mode=False):
    mapping = print_and_get_available_products(products)
    while choice.lower() != "n":
        product_id = int(input("Enter the product ID you want to buy: ")) - 1
        quantity = int(input("Choose quantity: "))

        updated_account = add_product_to_cart(product_id, products, mapping, quantity, account)
        total_price = updated_account['basket']["total_price"]
        if not guest_mode:
            update_account(updated_account)
        
        print(f"The current total price is £{total_price:.2f}")
        choice = input("Want to add another product? Y/n ")
        print(f'choice is {choice}')

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
        # print(total_price)


    delivery_details = {
        'address': address,
        'postcode': delivery_postcode,
    }

    complete_payment(account, delivery_details)


def add_product_to_cart(product_id, product_catalogue, product_map, quantity, account):
    name = product_map[product_id]
    price = product_catalogue[name]

    account['basket']['items'][name] = {}
    
    account['basket']['items'][name]["quantity"] = account['basket']['items'][name].get("quantity", 0) + quantity
    account['basket']['items'][name]["product_id"] = product_id
    account['basket']['items'][name]["price"] = price
    account['basket']['total_price'] += price



    return account

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

def update_account(account):
    existing_accounts = get_existing_accounts()
    existing_accounts[account['email']] = account

    with open('user_account.json', 'w') as accounts_file:
        json.dump(existing_accounts, accounts_file, indent=2)

main()