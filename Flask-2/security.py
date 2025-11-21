from user import User
import hmac  


def safe_str_cmp(a, b):
    """Safe string comparison to replace removed Werkzeug function."""
    return hmac.compare_digest(a, b)


def auth(username, password):
    user = User.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user
    return None


def identity(payload):
    id = payload['identity']
    return User.find_by_id(id)
