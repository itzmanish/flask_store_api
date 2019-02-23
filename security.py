from users import User
from werkzeug.security import generate_password_hash, check_password_hash

users = [
    User(1, 'manish', 'pbkdf2:sha256:50000$nmMkXOsz$1113d0057411909c6d69b2cedc7af760612dc11bf3f9e944b3ebfad5711da687')
]

username_mapping = {u.username: u for u in users}
userid_mapping = {u.id: u for u in users}


def authenticate(username, password):
    user = username_mapping.get(username, None)
    if user:
        if check_password_hash(user.password, password):
            return user
        else:
            print('no user found')

    print('authentication faiiled')


def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)


authenticate('manish', 'asdf')
