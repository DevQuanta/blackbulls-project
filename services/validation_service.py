import re

def validate_email(email):
    if re.search(r'\w+@\w+\.\w+', email) is None:
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