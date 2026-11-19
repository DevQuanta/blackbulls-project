from services.products_services import add_product_to_cart
from services.products_services import clear_basket as clear_basket_service
from ui.products_ui import print_and_get_available_products
from services.account_service import update_account
from environment import PRODUCTS
import questionary
from rich.console import Console


console = Console()


def browse_products(account, choice="Y", guest_mode=False):
    mapping = print_and_get_available_products(PRODUCTS)
    choices = [
        {"name": name, "value": idx} for idx, (_, name) in enumerate(mapping.items())
    ]

    while choice.lower() != "n":
        c_choices = [{"name": "Yes", "value": "Y"}, {"name": "No", "value": "N"}]
        product_id = int(
            questionary.select("Choose product: ", choices=choices).unsafe_ask()
        )
        quantity = questionary.text("Enter quantity: ").unsafe_ask()

        try:
            quantity = int(quantity)
        except:
            console.print("[bright_red]Invalid quantity entered here[/bright_red]")
            choice = questionary.select(
                "Add another product?", choices=c_choices
            ).unsafe_ask()

            continue

        updated_account = add_product_to_cart(
            product_id, PRODUCTS, mapping, quantity, account
        )
        if not updated_account:
            console.print("[bright_red]Invalid quantity entered[/bright_red]")
            choice = questionary.select(
                "Add another product?", choices=c_choices
            ).unsafe_ask()
            continue

        total_price = updated_account["basket"]["total_price"]
        if not guest_mode:
            update_account(updated_account)

        console.print(f"[green]Item added to basket[/green]")
        choice = questionary.select(
            "Add another product?", choices=c_choices
        ).unsafe_ask()


def clear_basket(account):
    confirmation = questionary.confirm(
        "Would you really like to clear basket?"
    ).unsafe_ask()

    if confirmation:
        clear_basket_service(account)
