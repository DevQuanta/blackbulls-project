products = {
     'Titos Homemade Vodka': 18.50,
     'Another Hendricks Gin': 33.50,
     'Aperol': 13.00,
     'Bumbu original': 38.50,
     'Forte Alto Pinot Grigio': 10.00,
     'Campari Bitters': 16.00,
     'Waitrose London Dry Gin': 20.25,
     'Louis Roederer Cristal': 280.00,
     'Dom Perigton Vintage': 210.00,
     'Dalmore 15 Year Old Single Malt': 111.00,
     'Star Hill Farm Whisky': 100.00,
 }

mapping = {}

import json
import random

from currency_exchange import convert_currency, symbols


def create_account():
    name = input("What is your name? ")
    email = input("What is your email? ")
    password = input("What is your password? ")
    repeat_password = input("Please confirm your password: ")
    while repeat_password != password:
        print("To confirm your password...you must type it out again.")
        password = input("Please input your password: ")
        repeat_password = input("Please confirm your password: ")
    account = {
        email: {
                'password': repeat_password,
                'Name': name,
        }
    }
    with open("user_account.json","w") as account_file:
        json.dump(account,account_file, indent = 2)
        account_file.flush() 
    


def main():
    create_account()
    total_price = 0
    for product_id, (name,price) in enumerate(products.items()):
        mapping[product_id] = name
        print(f'ID: {product_id}')
        print(f'Name: {name}')
        print(f'Price: £{price}\n')

    choice = input("Want to add a product? Y/n ")
    while choice.lower() != "n":
        product_id = int(input("Enter the product ID you want to buy: "))
        quantity = int(input("Choose quantity: "))
        name = mapping[product_id]
        price = products[name]
        total_price += price * quantity

        print(f"The current total price is £{total_price:.2f}")
        choice = input("Want to add a product? ")

    delivery_postcode = input("Enter your postcode: ")
    tax = random.randint(1,100)
    total_price += tax
    convert = input("Would you like to convert the final price to another currency? Y/n ")

    if convert.lower() == "y":
        all_currencies = symbols.keys()
        available_currencies = []
        for currency in all_currencies:
            if currency != "GBP":
                available_currencies.append(currency)
        for idx, currency in enumerate(available_currencies):
            print(f'{idx}.{currency}')

        new_currency_idx = int(input("What currency do you want it to be converted into? "))
        new_currency = available_currencies[new_currency_idx]
        total_price = convert_currency("GBP", new_currency, total_price)
        print(f"The new price is {total_price}")


main()

