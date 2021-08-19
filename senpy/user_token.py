import keyring

def set_token(new_token):
    """
    sets new token in the system

    parameters : 
    new_token : new value to the token 

    returns :
    """

    keyring.set_password("senpy_auth_token", "user", f"Token {new_token}")

def get_token():
    """
    reads the token and returns it

    parameters :

    returns :
    the value of the current token
    """

    return keyring.get_password("senpy_auth_token", "user")


def delete_token():
    """
    delete the stored token

    parameters :

    returns :
    """
    if get_token() is not None:
        keyring.delete_password("senpy_auth_token", "user")