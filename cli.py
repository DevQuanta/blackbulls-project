from rich.console import Console

from commands.basket_commands import checkout_basket
from commands.account_commands import create_account_command
from ui.products_ui import fetch_basket, diaplay_previous_orders
from commands.products_commands import browse_products, clear_basket
from commands.account_commands import login_account_command

import questionary
console = Console()

def go_to_basket(account, guest_mode=False):
    menu_items = ["View basket", "Clear basket", "Checkout basket", "Go back"]
    choices = [{
        'name': item, 'value': idx
    } for idx, item in enumerate(menu_items)]

    option_idx = questionary.select("Choose an action", choices=choices).unsafe_ask()
    
    while option_idx is not None and option_idx != 3:
        match option_idx:
            case 0:
                fetch_basket(account)
            case 1:
                clear_basket(account)
            case 2:
                checkout_basket(account, guest_mode)
            case 3:
                continue

        option_idx = questionary.select("Choose an action", choices=choices).unsafe_ask()

def logged_in_mode(account):
    console.print(f"[green]Welcome back, {account['name']}![/green]")

    menu_items = ["Go to basket", "Add product", "View previous orders", "Logout"]

    choices = [{
        'name': item, 'value': idx
    } for idx, item in enumerate(menu_items)]

    option_idx = questionary.select("Choose an action", choices=choices).unsafe_ask()
    
    while option_idx is not None:
        match option_idx:
            case 0:
                go_to_basket(account)
            case 1:
                browse_products(account)
            case 2:
                diaplay_previous_orders(account)
            case 3:
                break

        option_idx = questionary.select("Choose an action:", choices=choices).unsafe_ask()
                

def guest_mode():
    menu_items = ["Go to basket", "Add product", "Login", "Quit"]
    
    choices = [
        {"name": item, "value": idx} 
        for idx, item in enumerate(menu_items)
    ]

    option_idx = questionary.select("Choose an action", choices = choices).unsafe_ask()
    
    account = create_account_command(guest_account=True)
    
    while option_idx is not None:
        match option_idx:
            case 0:
                go_to_basket(account, guest_mode=True)
            case 1:
                browse_products(account)
            case 2:
                account = login_account_command()

                if account is None:
                    continue

                logged_in_mode(account)
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
