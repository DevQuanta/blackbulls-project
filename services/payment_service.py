from services.account_service import update_account
import random

def calculate_delivery_fees(distance):
    delivery_fees = 15
    if distance > 3000:
        delivery_fees = 100
    elif distance > 2000 and distance <= 3000:
        delivery_fees = 75
    elif distance > 1000 and distance <= 2000:
        delivery_fees = 50

    return delivery_fees

def get_pending_orders(account):
    pending_orders = []
    for order in account.get("orders", []):
        if order.get("payment_status") == "pending":
            pending_orders.append(order.get("order_id"))

    return pending_orders

def create_pending_order(account, guest_mode=False):
    order_id = f"TX_{random.randint(1000000, 99999999)}"

    order = {
            'order_id': order_id,
            'items': account["basket"]["items"],
            'delivery_details': {
                'address': '',
                'postcode': ''
            },
            'total_price': account["basket"]["total_price"],
            'payment_status': 'pending'
        }

    account["orders"].append(order)

    if not guest_mode:
        update_account(account)
    
    return order_id


def complete_payment(account, delivery, card_details, order_id, pending=False, guest_mode=False):

    for idx, order in enumerate(account.get("orders", [])):
        if order.get("order_id") == order_id:
            print('here matching')
            account["orders"][idx] = {
                'order_id': order["order_id"],
                'items': order["items"],
                'delivery_details': {
                    'address': delivery["address"],
                    'postcode': delivery["postcode"]
                },
                'total_price': order["total_price"],
                'payment_status': 'completed'
            }

            print(order)

    if not guest_mode:
        update_account(account)

    if not pending:
        account["basket"]["items"] = {}
        account["basket"]["total_price"] = 0
        account["basket"]["tax"] = 0

    return True
    
