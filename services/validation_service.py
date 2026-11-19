import re

def validate_cvv(cvv):
    if re.search(r'^\d{3}$', cvv) is None:
        return "Invalid CVV"

    else:
        return True


def validate_card_number(card_number):
    if re.search(r'^\d{16}$', card_number)is None:
        return "Invalid card number"

    else:
        return True

def validate_expiry(expiry):
    if re.search(r'^(0[1-9]|1[0-2])/(2[7-9]|[34][0-9]|50)$', expiry) is None:

        return "Invalid expiry date"

    else:
        return True


def validate_email(email):
    if re.search(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email) is None:
        return "Invalid email address"

    else:
        return True

def validate_password(password):
    if len(password) < 8:
        return "Password length must be greater than 8 characters"

    elif re.search('[0-9]', password) is None:
        return "Password must contain at least one digit"

    else:
        return True

def validate_quantity(quantity):
    return quantity > 0
