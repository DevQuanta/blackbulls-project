from services.products_services import browse_products
from services.display_service import fetch_basket
from services.account_service import get_account, create_account, fetch_orders
from services.payment_service import checkout_basket

import questionary

def logged_in_mode(account):
    print(f"Welcome back, {account['name']}!\n")

    menu_items = ["View basket", "Checkout basket", "Add products", "View previous orders", "Logout"]

    choices = [{
        'name': item, 'value': idx
    } for idx, item in enumerate(menu_items)]

    option_idx = questionary.select("Choose an action", choices=choices).ask()
    
    while option_idx is not None:
        match option_idx:
            case 0:
                fetch_basket(account)
            case 1:
                checkout_basket(account)
            case 2:
                browse_products(account)
            case 3:
                fetch_orders(account)
            case 4:
                break

        option_idx = questionary.select("Choose an action:", choices=choices).ask()
                

def guest_mode():
    menu_items = ["View basket", "Checkout basket", "Add products", "Quit"]
    
    choices = [
        {"name": item, "value": idx} 
        for idx, item in enumerate(menu_items)
    ]

    # option = input("Would you like to:\n1. View basket\n2. Checkout basket\n3. Add products\n4. Quit\n> ")
    option_idx = questionary.select("Choose an action", choices = choices).ask()
    
    account = create_account(guest_account=True)
    
    while option_idx is not None:
        match option_idx:
            case 0:
                fetch_basket(account)
            case 1:
                checkout_basket(account)
            case 2:
                browse_products(account, guest_mode = True)
            case 3:
                break

        # option = input("Would you like to:\n1. View basket\n2. Checkout basket\n3. Add products\n4. Quit\n> ")

        option_idx = questionary.select("What would you like to do?", choices = choices).ask()

def main():
    menu_items = ["Sign in", "Create an account", "Continue as guest", "Quit"]
        
    choices = [
        {"name": item, "value": idx} 
        for idx, item in enumerate(menu_items)
    ]

    option_idx = questionary.select("Choose an action:", choices=choices).ask()

    while option_idx is not None:

        match option_idx:
            case 0:
                email = questionary.text("Please enter your email: ").ask()
                password = questionary.password("Please enter your password: ").ask()
                account = get_account(email, password)

                while account is None:
                    print("Incorrect email or password. Please try again!\n")
                    email = questionary.text("Please enter your email: ").ask()
                    password = questionary.password("Please enter your password: ").ask()
                    account = get_account(email, password)

                logged_in_mode(account)

            case 1:
                account = create_account()
                logged_in_mode(account)

            case 2:
                guest_mode()

            case 3:
                break
        
        option_idx = questionary.select("Choose an action:", choices=choices).ask()
    
main()