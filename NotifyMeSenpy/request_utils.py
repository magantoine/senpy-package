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
    return req.content

def post(tail, content):
    """
    performs a post request to the server with percise root and content

    parameters:
    tail : the root to the query
    content : the content to post

    returns :
    the response to the request
    """
    req = requests.post(create_url(tail), content)
    return req.content

