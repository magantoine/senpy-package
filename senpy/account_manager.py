from __future__ import print_function, unicode_literals
from PyInquirer import prompt, style_from_dict, Token, Validator, ValidationError
from .request_utils import post
from colorama import Fore, Style
import argparse
from .user_token import get_token, set_token
from enum import Enum 

__default_func = lambda x : None

class Status(Enum):
    """
    enum for status return
    """
    SUCCESS = 0
    FAILURE = 1

class Result:
    """
    result of a query
    """
    def __init__(self, status, message):
        self.status = status ## failure or success 
        self.message = message ## message of the result

class PasswordValidator(Validator):
    def validate(self, document):
        if len(document.text) < 8:
            raise ValidationError(
                message='At least 8 characters',
                cursor_position=len(document.text))  # Move cursor to end


username =  [{
            'type': 'input',
            'message': 'Username',
            'name': 'username', #The name of the question is the request body key
        }]
password = [{
            'type': 'password',
            'message': 'Password',
            'name': 'password',
            'validate': PasswordValidator
        }]

def register(on_success=__default_func, on_failure=__default_func):
    """
    register to the server

    parameters:
    on_success = callback called when the request succeeds
    on_failure = callback called when the requests fails
    """
    questions = username + password + [
        {
            'type': 'password',
            'message': 'Password confirmation',
            'name': 'password_confirmation',
        }]
    registered = False
    while not registered:
        data = prompt(questions)
        print("========================================")
        print(data)
        print("========================================")
        res = post('api/auth/register', data)
        if res.status_code == 201:
            token = res.json()['auth_token']
            set_token(token)
            user_id = res.json()['id']
            on_success(res)
            registered = True
            return Result(Status.SUCCESS, 'Account created')
            
        else:
            #print_error(res)
            on_failure(res)
    return Result(Status.FAILURE, res)


def login(on_success=__default_func, on_failure=__default_func):
    """
    login to the server

    parameters:
    on_success = callback called when the request succeeds
    on_failure = callback called when the requests fails
    """
    logged_in = False
    while not logged_in:
        data = prompt(username + password)
        res = post('api/auth/login', data)
        if res.status_code == 200:
            token = res.json()['auth_token']
            set_token(token)
            logged_in = True
            on_success(res)
            return Result(Status.SUCCESS, "You are logged in, welcome!")
        else:
            on_failure(res)
    
    return Result(Status.FAILURE, res)

def logout(on_success=__default_func, on_failure=__default_func):
    """
    logout from the server

    parameters:
    on_success = callback called when the request succeeds
    on_failure = callback called when the requests fails
    """
    token = get_token()
    res = post('api/auth/logout', headers={'Authentication': token})
    on_success(res)
    return Result(Status.SUCCESS, "You are logged out, see you!")
    
def change_password(on_success=__default_func, on_failure=__default_func):
    """
    change password in the server

    parameters:
    on_success = callback called when the request succeeds
    on_failure = callback called when the requests fails
    """
    questions = [
        {
            'type': 'password',
            'message': 'Current password',
            'name': 'current_password',
        },
        {
            'type': 'password',
            'message': 'New password',
            'name': 'new_password',
        },
        {
            'type': 'password',
            'message': 'Confirmation',
            'name': 'new_password_confirmation',
        }
    ]
    success = False
    token = get_token()
    while not success:
        data = prompt(questions)
        res = post('api/auth/change_password', data, headers={'Authorization':token})
        if res.status_code == 204:
            on_success(res)
            success = True
            return Result(Status.SUCCESS, 'Password changed successfully.')
        else:
            on_failure(res)
    return Result(Status.FAILURE, res)

def delete_account(on_success=__default_func, on_failure=__default_func):
    """
    delete account in the server

    parameters:
    on_success = callback called when the request succeeds
    on_failure = callback called when the requests fails
    """
    token = get_token()
    logged_in = False
    while not logged_in:
        data = prompt(username + password)
        res = post('api/auth/delete', data, headers={'Authorization':token})
        if res.status_code == 200:
            on_success(res)
            logged_in = True
            return Result(Status.SUCCESS, "Account deleted successfully.")
        else:
            on_failure(res)
    return Result(Status.FAILURE, res)
