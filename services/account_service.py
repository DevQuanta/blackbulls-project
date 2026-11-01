import json
from environment import ACCOUNT_FILE
from services.password_service import generate_hash, check_password

def create_account(name, email, password, guest_account = False):
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
    summary = []

    for order in account.get('orders', {}):
            order_summary = {}
            order_summary['order_id'] = order["order_id"]
            order_summary['products'] = []
            
            for name, product in order["items"].items():
                product = {
                    'id': product["product_id"],
                    'name': name,
                    'quantity': product["quantity"],
                    'price': product['price']
                }

                order_summary['products'].append(product)

            order_summary['delivery_details'] = {
                'address': order["delivery_details"]["address"],
                'postcode': order["delivery_details"]["postcode"],
            }

            order_summary['billing_payment'] = {
                'total_price': order["total_price"],
                'payment_status': order["payment_status"]
            }

            summary.append(order_summary)

    print(summary)