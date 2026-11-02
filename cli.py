from commands.basket_commands import checkout_basket
from commands.account_commands import create_account_command
from ui.products_ui import fetch_basket, diaplay_previous_orders
from commands.products_commands import browse_products
from commands.account_commands import login_account_command

import questionary

def logged_in_mode(account):
    print(f"Welcome back, {account['name']}!\n")

    menu_items = ["View basket", "Checkout basket", "Add products", "View previous orders", "Logout"]

    choices = [{
        'name': item, 'value': idx
    } for idx, item in enumerate(menu_items)]

    option_idx = questionary.select("Choose an action", choices=choices).unsafe_ask()
    
    while option_idx is not None:
        match option_idx:
            case 0:
                fetch_basket(account)
            case 1:
                checkout_basket(account)
            case 2:
                browse_products(account)
            case 3:
                diaplay_previous_orders(account)
            case 4:
                break

        option_idx = questionary.select("Choose an action:", choices=choices).unsafe_ask()
                

def guest_mode():
    menu_items = ["View basket", "Checkout basket", "Add products", "Quit"]
    
    choices = [
        {"name": item, "value": idx} 
        for idx, item in enumerate(menu_items)
    ]

    option_idx = questionary.select("Choose an action", choices = choices).unsafe_ask()
    
    account = create_account_command(guest_account=True)
    
    while option_idx is not None:
        match option_idx:
            case 0:
                fetch_basket(account)
            case 1:
                checkout_basket(account, guest_mode=True)
            case 2:
                browse_products(account, guest_mode=True)
            case 3:
                break

        option_idx = questionary.select("What would you like to do?", choices = choices).unsafe_ask()

def main():
    try:
        menu_items = ["Sign in", "Create an account", "Continue as guest", "Quit"]
            
        choices = [
            {"name": item, "value": idx} 
            for idx, item in enumerate(menu_items)
        ]

        option_idx = questionary.select("Choose an action:", choices=choices).unsafe_ask()

        while option_idx is not None:

            match option_idx:
                case 0:
                    account = login_account_command()

                    if account is None:
                        continue

                    logged_in_mode(account)

                case 1:
                    account = create_account_command()

                    if account is None:
                        continue

                    logged_in_mode(account)

                case 2:
                    guest_mode()

                case 3:
                    break
            
            option_idx = questionary.select("Choose an action:", choices=choices).unsafe_ask()
    except KeyboardInterrupt:
        print("Gracefully exiting application")
    
main()