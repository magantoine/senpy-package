### UTILS FOR REQUEST THE SERVER
import requests


_URL = "http://127.0.0.1:8000/{}"

def create_url(tail):
    return _URL.format(tail)

def get_base_url():
    return _URL.format("")

def get(tail):
    """
    performs a get request to the server with percise root

    parameters:
    tail : the root to the query

    returns :
    the response to the request
    """
    req = requests.get(create_url(tail))
    return req # Content is of type byte

def post(tail, body=None, headers=None):
    """
    performs a post request to the server with percise root and body

    parameters:
    tail : the root to the query
    body : dict, the content to post

    returns :
    the response to the request
    """
    req = requests.post(create_url(tail), data=body, headers=headers)
    return req # Content is of type byte

