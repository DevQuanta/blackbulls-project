from services.display_service import print_and_get_available_products
from environment import PRODUCTS
from services.account_service import update_account


def browse_products(account, choice="Y", guest_mode=False):
    mapping = print_and_get_available_products(PRODUCTS)
    while choice.lower() != "n":
        product_id = int(input("Enter the product ID you want to buy: ")) - 1
        quantity = int(input("Choose quantity: "))

        updated_account = add_product_to_cart(product_id, PRODUCTS, mapping, quantity, account)
        total_price = updated_account['basket']["total_price"]
        if not guest_mode:
            update_account(updated_account)
        
        print(f"The current total price is £{total_price:.2f}")
        choice = input("Want to add another product? Y/n ")
        print(f'choice is {choice}')

def add_product_to_cart(product_id, product_catalogue, product_map, quantity, account):
    name = product_map[product_id]
    price = product_catalogue[name]

    account['basket']['items'][name] = {}
    
    account['basket']['items'][name]["quantity"] = account['basket']['items'][name].get("quantity", 0) + quantity
    account['basket']['items'][name]["product_id"] = product_id
    account['basket']['items'][name]["price"] = price
    account['basket']['total_price'] += price



    return account