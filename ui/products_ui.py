from rich.console import Console
from rich.table import Table

console = Console()


def fetch_basket(account):
    table = Table(title = "Basket", min_width=100)

    table.add_column("Product ID", justify = "right", style = "cyan", no_wrap = True)
    table.add_column("Product Name", style = "magenta")
    table.add_column("Price", justify = "left", style = "green")
    table.add_column("Quantity", justify = "left", style = "orange3")

    for name, product in account.get('basket', {}).get('items', {}).items():
        table.add_row(f"{product["product_id"]}", name, f"£{product["price"]}", f"{product["quantity"]}")

    table.add_column("Total", justify="right", footer=f"£{account["basket"]["total_price"]}", style="green")
    console.print(table)


def print_and_get_available_products(product_catalogue):
    mapping = {}
    table = Table(title = "Product catalogue", min_width=100)


    table.add_column("Product ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Name", style="magenta")
    table.add_column("Price", justify="left", style="green")

    for product_id, (name,price) in enumerate(product_catalogue.items()):
        mapping[product_id] = name
        product_id += 1

        table.add_row(str(product_id), name, f"£{price}")

    console.print(table)
    return mapping
