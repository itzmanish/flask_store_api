from users import User
from werkzeug.security import generate_password_hash, check_password_hash
# users = [
#     User(1, 'manish', 'pbkdf2:sha256:50000$nmMkXOsz$1113d0057411909c6d69b2cedc7af760612dc11bf3f9e944b3ebfad5711da687')
# ]


def generate_password(password):
    hased = generate_password_hash(
        password, method='pbkdf2:sha256', salt_length=10)
    return hased


def authenticate(username, password):
    user = User.find_by_username(username)
    if user:
        if check_password_hash(user.password, password):
            return user
        else:
            return 'Authentication failed', 401

    print('No user exists with this username')


def identity(payload):
    user_id = payload['identity']
    return User.find_by_id(user_id)


# authenticate('manish', 'asdf')
