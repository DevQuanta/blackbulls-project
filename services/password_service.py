import bcrypt

def generate_hash(password):
    # converting password to array of bytes
    bytes = password.encode('utf-8')

    # generating the salt
    salt = bcrypt.gensalt()

    # Hashing the password
    hash = bcrypt.hashpw(bytes, salt)

    return hash

def check_password(password, expected_hash):
    userBytes = password.encode('utf-8')
    return bcrypt.checkpw(userBytes, expected_hash.encode('utf-8'))
