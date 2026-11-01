from services.products_services import add_product_to_cart
from ui.products_ui import print_and_get_available_products
from services.account_service import update_account
from environment import PRODUCTS

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