### UTILS FOR REQUEST THE SERVER
import requests
from .user_token import get_token

_URL = "http://192.168.43.175:8000/api/{}"

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

def post(tail, json=None, headers=None):
    """
    performs a post request to the server with percise root and body

    parameters:
    tail : the root to the query
    body : dict, the content to post
    json : json, the content to post

    returns :
    the response to the request
    """
    if headers is None:
        headers = {"Content-Type":"application/json"}
        token = get_token()
        if token is not None:
            headers["Authorization"] = token

    try:
        req = requests.post(create_url(tail), json=json, headers=headers)
        return req # Content is of type byte
    except Exception as err:
        return {
            'python_error' : True, 
            'exception': str(err),
            'message':"Server unreachable, make sure you are connected to internet"
        }

def put(tail, json=None, headers=None):
    """
    performs a put request to the server with precise root and body

    parameters:
    tail : the root to the query
    body : dict, the content to post
    json : json, the content to post

    returns :
    the response to the request
    """
    if headers is None:
        headers = {"Content-Type":"application/json"}
        token = get_token()
        if token is not None:
            headers["Authorization"] = token

    try:
        req = requests.put(create_url(tail), json=json, headers=headers)
        return req # Content is of type byte
    except Exception as err:
        return {
            'python_error' : True, 
            'exception': str(err),
            'message':"Server unreachable, make sure you are connected to internet"
        }

def handle_request_error(res):
    #Import here to avoid cyclic import (source: https://stackoverflow.com/a/33547682)
    from .cli import print_error
    print_error(res)