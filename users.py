class User:
    """
    class for creating new user object. 
    this should be in format of
    user(id, username, password)
    """

    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password
