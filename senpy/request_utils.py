### UTILS FOR REQUEST THE SERVER
import os
import sys
import colorama
from colorama import Fore, Style, AnsiToWin32
import requests
from requests.exceptions import Timeout
from .user_token import get_token

import asyncio

colorama.init(convert=True)
stream = AnsiToWin32(sys.stderr).stream
_URL = "https://api.senpy.ch/api/{}"

def create_url(tail):
    return _URL.format(tail)

def get_base_url():
    return _URL.format("")

def request_handler(tail, request_func, json=None, headers=None):
    if headers is None:
        headers = {"Content-Type":"application/json"}
        token = get_token()
        if token is not None:
            headers["Authorization"] = token
    
    try:
        req = request_func(create_url(tail), headers=headers, json=json, timeout=5)
        return req # Content is of type byte
    except (Timeout, Exception) as err:
        return {
            'python_error' : True, 
            'exception': str(err),
            'message':"Server unreachable, make sure you are connected to internet"
        }


async def async_request_handler(tail, request_type, json=None, headers=None, on_success=lambda x : None, on_error=lambda x : None):
    
    if headers is None:
        headers = {"Content-Type":"application/json"}
        token = get_token()
        if token is not None:
            headers["Authorization"] = token
    print("1")
    async with aiohttp.ClientSession() as session:
        print("2")
        full_URL = create_url(tail)

        func = session.get if request_type == "GET" else session.post if request_type == "POST" else session.put
        try :
            print("3")
            async with func(full_URL, headers=headers, json=json, timeout=5) as response:
                content = await response.json()
                print("4")
                if(content.status_code == 200):
                    ## success we can apply the success part here
                    on_success(content)
                else :
                    ## we have an error 
                    on_error(content)
        except (Timeout, Exception) as err:
            ## timeout error is triggered
            err_arg = {
            'python_error' : True, 
            'exception': str(err),
            'message':"Server unreachable, make sure you are connected to internet"
            }
            on_error(err_arg)
    


def get(tail, headers=None):
    """
    performs a get request to the server with percise root

    parameters:
    tail : the root to the query

    returns :
    the response to the request
    """
    return request_handler(tail, requests.get, headers=headers)

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
    return request_handler(tail, requests.post, json=json, headers=headers)

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
    return request_handler(tail, requests.put, json=json, headers=headers)

def handle_request_error(res):
    #Import here to avoid cyclic import (source: https://stackoverflow.com/a/33547682)
    from .cli import print_error
    print_error(res)

   
def print_error(res):
    """

    prints error message 

    parameters :
    res : result of the query
    """
    def print_message(error, header=None, helpers=None):
        print(Fore.RED + "Senpy - " + error.lower() + Style.RESET_ALL, file=stream)
        if(helpers is not None):
            ## help is provided

            print(Fore.LIGHTYELLOW_EX + ("Possible fix" if header is None else header) + " : ", file=stream)
            for help in helpers :
                print("\t - " + help, file=stream)
            print(Style.RESET_ALL, file=stream)


    if type(res) == str:
        print_message(res)

    elif 'python_error' in res:
        print_message(res['message'])

    elif res.status_code == 429:
        helps = ["Try again later", "You are probably trying to sending notify_me requests to frequently", "You're iterations might be too quick"]
        print_message(error="Too many requests", helpers=helps)

    elif res.status_code == 500:
        report = ["Try again later", "contact us at notify.me.senpy@gmail.com", "report the issue at https://github.com/magantoine/senpy-package"]
        print_message("An error occurred on our side, please try again later.", header="If the problem persists", helpers=report)


    else:
        data = res.json()
        if type(data) == list:
            for error in data:
                print_message(error)
        elif type(data) == dict:
            for key, errors in data.items():
                if type(errors) == list:
                    for error in errors:
                        print_message(f"{key}: {error}")
                elif type(errors) == str:
                    print_message(f"{key}: {errors}")
        else:
            print_message(str(data))

def print_success(message):
    """

    prints succes of a query

    parameters :
    message : message to print
    """
    print(Fore.GREEN + message + Style.RESET_ALL)




