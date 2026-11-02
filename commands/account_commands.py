import questionary
from services.validation_service import validate_password, validate_email
from services.account_service import create_account, get_account, create_guest_account
from rich.console import Console
from rich.table import Table

console = Console()

def login_account_command():
    email = questionary.text("Please enter your email: ").unsafe_ask()
    password = questionary.password("Please enter your password: ").unsafe_ask()
    account = get_account(email, password)

    while account is None:
        print("Incorrect email or password. Please try again!\n")
        email = questionary.text("Please enter your email: ").unsafe_ask()
        password = questionary.password("Please enter your password: ").unsafe_ask()
        account = get_account(email, password)

    return account

def create_account_command(guest_account = False):
    if guest_account:
        return create_guest_account()
    else:
        name = questionary.text("What is your name? ").unsafe_ask()
        email = questionary.text("What is your email? ", validate=validate_email).unsafe_ask()
        password = questionary.password("What is your password? ", validate=validate_password).unsafe_ask()
        repeat_password = questionary.password("Please confirm your password: ").unsafe_ask()

        while repeat_password != password:
            print("To confirm your password...you must type it out again.")
            password = questionary.password("What is your password? ", validate=validate_password).unsafe_ask()
            repeat_password = questionary.password("Please confirm your password: ").unsafe_ask()

        return create_account(name, email, password)