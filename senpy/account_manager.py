from __future__ import print_function, unicode_literals
from InquirerPy import prompt
from prompt_toolkit.validation import Validator, ValidationError
from .request_utils import post
import argparse
from .user_token import get_token, set_token, delete_token
from enum import Enum 
from .request_utils import print_success, print_error
from colorama import Fore, Style, AnsiToWin32
import sys

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
            'validate': PasswordValidator()
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




    
    disclaimers ="""This is a beta version. We do not give any warranties, whether express or implied, as to the suitability or usability of the app,
its software or any of its content. We will not be liable for any loss, whether such loss is direct, indirect, special or consequential, 
suffered by any party as a result of their use of the beta app, its content and functionalities."""

    disclaimers += Fore.LIGHTYELLOW_EX + "\nDon't share any sensitive information on SenPy.\n" + Style.RESET_ALL
    ### PROMPT THE DISCLAIMER :
    print(Fore.LIGHTYELLOW_EX + "DISCLAIMERS :" + Style.RESET_ALL, file=AnsiToWin32(sys.stderr).stream)
    print(disclaimers)
    while not registered:
        data = prompt(questions)
        res = post('auth/register', data)
        if 'python_error' not in res and res.status_code == 200:
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
        res = post('auth/login', json=data)
        if 'python_error' not in res and res.status_code == 200:
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
    question = {
        'type':'confirm',
        'message':"Logging out will interrupt any job updates currently running. \nDo you still want to log out?",
        'name':'confirmation'
    }
    data = prompt(question)
    if data['confirmation'] == False:
        #User doesn't want to logout anymore
        return
    res = post('auth/logout')
    on_success(res)
    delete_token()
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
    while not success:
        data = prompt(questions)
        res = post('auth/change_password', data)
        if 'python_error' not in res and res.status_code == 200:
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
    question = {
        'type':'confirm',
        'message':"Deleting the account will interrupt any job updates currently running. \nDo you want to continue?",
        'name':'confirmation'
    }
    data = prompt(question)
    if data['confirmation'] == False:
        #User doesn't want to delete account anymore
        return

    logged_in = False
    while not logged_in:
        data = prompt(username + password)
        res = post('auth/delete', data)
        if 'python_error' not in res and res.status_code == 200:
            on_success(res)
            logged_in = True
            delete_token()
            return Result(Status.SUCCESS, "Account deleted successfully.")
        else:
            on_failure(res)
    return Result(Status.FAILURE, res)

def check_token_exists():
    if get_token() != None:
        return
    choices = ['Create an account', 'I already have an account']
    question = {
        'type': 'list',
        'message': 'It looks like you are not logged in a senpy account!',
        'name': 'register_or_login',
        'choices': choices,
        'default': 0
    }
    data = prompt(question)
    if data['register_or_login'] == choices[0]:
        #First choice is register
        register(on_success=lambda res : print_success('Account created!'), on_failure=print_error)
    else:
        login(on_success=lambda res : print_success("You are logged in, welcome!"), on_failure=print_error)