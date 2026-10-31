import json
from environment import ACCOUNT_FILE
import questionary
from services.validation_service import validate_email, validate_password
from services.password_service import generate_hash, check_password

def create_account(guest_account = False):
    if guest_account:
        return {
                    'name': 'Guest',
                    'basket': {
                        'items': {},
                        'total_price': 0,
                        'tax': 0
                    },
                    'orders': []
                }
  
    name = questionary.text("What is your name? ").ask()
    email = questionary.text("What is your email? ", validate=validate_email).ask()
    password = questionary.password("What is your password? ", validate=validate_password).ask()
    repeat_password = questionary.password("Please confirm your password: ").ask()

    while repeat_password != password:
        print("To confirm your password...you must type it out again.")
        password = questionary.password("What is your password? ", validate=validate_password).ask()
        repeat_password = questionary.password("Please confirm your password: ").ask()

    hashed = generate_hash(password).decode()
    
    account = {
        'name': name,
        'email': email,
        'password': hashed,
        'basket': {
            'items': {},
            'total_price': 0,
            'tax': 0
        },
        'orders': []
    }

    update_account(account)
    return account 


def get_existing_accounts():
    try:
        with open(ACCOUNT_FILE, "r") as account_file:
            existing_accounts = json.load(account_file)
    except:
        existing_accounts = {}

    return existing_accounts


def get_account(email, password):
    existing_accounts = get_existing_accounts()
    account = existing_accounts.get(email)
    if not account:
        return None
    
    stored_hash = account.get('password', '')

    if stored_hash and check_password(password, stored_hash):
        return existing_accounts.get(email)

    return None


def update_account(account):
    existing_accounts = get_existing_accounts()
    existing_accounts[account['email']] = account

    with open('user_account.json', 'w') as accounts_file:
        json.dump(existing_accounts, accounts_file, indent=2)

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

