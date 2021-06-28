import keyring

def set_token(new_token):
    """
    sets new token in the system

    parameters : 
    new_token : new value to the token 

    returns :
    """

    keyring.set_password("senpy", "userX", new_token)

def get_token():
    """
    reads the token and returns it

    parameters :

    returns :
    the value of the current token
    """

    return keyring.get_password("senpy", "userX")

