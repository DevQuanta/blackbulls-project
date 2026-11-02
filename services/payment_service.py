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

def save_delivery_details(account, order_id, delivery):
    save_idx = None
    for idx, order in enumerate(account.get("orders", [])):
        if order["order_id"] == order_id:
            save_idx = idx
            break

    account.get("orders", [])[save_idx]["delivery_details"] = delivery
    update_account(account)

    return True

def create_pending_order(account, symbol, total_price, guest_mode=False):
    order_id = f"TX_{random.randint(1000000, 99999999)}"

    order = {
            'order_id': order_id,
            'items': account["basket"]["items"],
            'delivery_details': {
                'address': '',
                'postcode': ''
            },
            'total_price': total_price,
            'symbol': symbol, 
            'payment_status': 'pending'
        }

    account["orders"].append(order)

    if not guest_mode:
        update_account(account)
    
    return order_id


def complete_payment(account, card_details, order_id, pending=False, guest_mode=False):

    print(f'we are completing the payment, guest_mode = {guest_mode}')
    for idx, order in enumerate(account.get("orders", [])):
        if order.get("order_id") == order_id:
            account["orders"][idx] = {
                'order_id': order["order_id"],
                'items': order["items"],
                'delivery_details': {
                    'address': order["delivery_details"]["address"],
                    'postcode': order["delivery_details"]["postcode"]
                },
                'total_price': order["total_price"],
                'symbol': order["symbol"], 
                'payment_status': 'completed'
            }

            print(order)

    if guest_mode:
        return True

    update_account(account)

    if not pending:
        account["basket"]["items"] = {}
        account["basket"]["total_price"] = 0
        account["basket"]["tax"] = 0

    return True
    
