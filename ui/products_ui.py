from rich.console import Console
from rich.table import Table
from services.account_service import fetch_orders

console = Console()

def fetch_basket(account):
    table = Table(title = "Basket", min_width=100, show_footer=True)

    table.add_column("Product ID", justify = "right", style = "cyan", no_wrap = True)
    table.add_column("Product Name", style = "magenta")
    table.add_column("Price", justify = "left", style = "green")
    table.add_column("Quantity", justify = "left", style = "orange3")
    table.add_column("Total", justify="right", footer=f"£{account['basket']['total_price']}", style="green")

    for name, product in account.get('basket', {}).get('items', {}).items():
        item_total = f"£{float(product['price']) * int(product['quantity'])}"
        table.add_row(f"{product['product_id']}", name, f"£{product['price']}", f"{product['quantity']}", item_total)
        
    console.print(table)


def print_and_get_available_products(product_catalogue):
    mapping = {}
    table = Table(title = "Product catalogue", min_width=100)


    table.add_column("Product ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Name", style="magenta")
    table.add_column("Price", justify="left", style="green")

    for product_id, (name, price) in enumerate(product_catalogue.items()):
        mapping[product_id] = name
        product_id += 1

        table.add_row(str(product_id), name, f"£{price}")

    console.print(table)
    return mapping


def diaplay_previous_orders(account):
    order_summary = fetch_orders(account)

    for order in order_summary:
        if order["billing_payment"]["payment_status"] == "pending":
            continue

        console.print(f"[bold bright_black]Order[/bold bright_black] #{order["order_id"]}")
        console.print(f"[bold bright_black]Address[/bold bright_black]")
        console.print(f"{order['delivery_details']['address']}, {order['delivery_details']['postcode']}")
        console.print(f"[bold bright_black]Billing details[/bold bright_black]")
        console.print(f"Price paid: {order["billing_payment"]["symbol"]}{order["billing_payment"]["total_price"]}")
        console.print(f"Payment status: {order["billing_payment"]["payment_status"]}")

        products_table = Table(min_width=100)

        console.print(f"[bold bright_black]Ordered Items[/bold bright_black]")
        products_table.add_column("Product ID", justify = "right", style = "cyan", no_wrap = True)
        products_table.add_column("Product Name", style = "magenta")
        products_table.add_column("Price", justify = "left", style = "green")
        products_table.add_column("Quantity", justify = "left", style = "orange3")
        products_table.add_column("Total", justify="right", footer=f"£{account['basket']['total_price']}", style="green")
    
        for product in order["products"]:
            item_total = f"£{float(product['price']) * int(product['quantity'])}"
            products_table.add_row(f"{product['product_id']}", f"{product['name']}", f"£{product['price']}", f"{product['quantity']}", item_total)

        console.print(products_table)