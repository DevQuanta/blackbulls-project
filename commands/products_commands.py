from services.products_services import add_product_to_cart
from ui.products_ui import print_and_get_available_products
from services.account_service import update_account
from environment import PRODUCTS
import questionary
from rich.console import Console

console = Console()

def browse_products(account, choice="Y", guest_mode=False):
    mapping = print_and_get_available_products(PRODUCTS)
    choices = [{
        'name': name,
        'value': idx
    } for idx, (_, name) in enumerate(mapping.items())]

    while choice.lower() != "n":
        product_id = int(questionary.select("Choose product: ", choices=choices).ask())
        quantity = questionary.text("Enter quantity: ").ask()

        try:
            quantity = int(quantity)
        except:
            console.print("[bright_red]Invalid quantity entered[/bright_red]")
            choice = questionary.select("Add another product?", choices = choices).ask()
            continue

        updated_account = add_product_to_cart(product_id, PRODUCTS, mapping, quantity, account)
        if not updated_account:
            console.print("[bright_red]Invalid quantity entered[/bright_red]")
            choice = questionary.select("Add another product?", choices = choices).ask()
            continue
        total_price = updated_account['basket']["total_price"]
        if not guest_mode:
            update_account(updated_account)
        
        console.print(f"[green]Item added to basket[/green]")
        choices = [{'name': 'Yes', 'value': 'Y'}, {'name': 'No', 'value': 'N'}]
        choice = questionary.select("Add another product?", choices = choices).ask()