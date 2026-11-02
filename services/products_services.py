from services.validation_service import validate_quantity

def add_product_to_cart(product_id, product_catalogue, product_map, quantity, account):
    name = product_map[product_id]
    price = product_catalogue[name]

    if not validate_quantity(quantity):
        return None
    
    account['basket']['items'][name] = {}
    
    account['basket']['items'][name]["quantity"] = account['basket']['items'][name].get("quantity", 0) + quantity
    account['basket']['items'][name]["product_id"] = product_id
    account['basket']['items'][name]["price"] = price


    account['basket']['total_price'] += price * quantity

    return account