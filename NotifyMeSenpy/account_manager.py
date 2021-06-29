from __future__ import print_function, unicode_literals
from PyInquirer import prompt, style_from_dict, Token, Validator, ValidationError
from .request_utils import post
from colorama import Fore, Style
import argparse
import user_token
from enum import Enum 


## enum for status return
class Status(Enum):
    SUCCESS = 0
    FAILURE = 1

class Result:
    def __init__(self, status, message):
        self.status = status 
        self.message = message

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

def register(on_success, on_failure, tries=200):
    questions = username + password + [
        {
            'type': 'password',
            'message': 'Password confirmation',
            'name': 'password_confirmation',
        }]
    registered = False
    while not registered and tries > 0:
        data = prompt(questions)
        res = post('api/auth/register', data)
        if res.status_code == 201:
            token = res.json()['auth_token']
            user_token.set_token(token)
            user_id = res.json()['id']
            # print(user_id)
            #print_success('Account created!')
            on_success(res)
            registered = True
            return Result(Status.SUCCESS, 'Account created')
            
        else:
            #print_error(res)
            on_failure(res)
        tries -= 1
    return Result(Status.FAILURE, res)


def login(on_success, on_failure, tries=200):
    logged_in = False
    while not logged_in and tries > 0:
        data = prompt(username + password)
        res = post('api/auth/login', data)
        if res.status_code == 200:
            #print_success("You are logged in, welcome!")
            token = res.json()['auth_token']
            user_token.set_token(token)
            logged_in = True
            on_success(res)
            return Result(Status.SUCCESS, "You are logged in, welcome!")
        else:
            #print_error(res)
            on_failure(res)
        tries -= 1
    
    return Result(Status.FAILURE, res)

def logout(on_success, on_failure, tries=200):
    #token = '2882ede988f3961c706dcc39320f4665160a2e67'
    token = user_token.get_token()
    res = post('api/auth/logout', headers={'Authentication': token})
    #print_success("You are logged out, see you!")
    on_success(res)
    return Result(Status.SUCCESS, "You are logged out, see you!")
    
def change_password(on_success, on_failure, tries=200):
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
    #token = 'Token 2882ede988f3961c706dcc39320f4665160a2e67'
    token = user_token.get_token()
    while not success and tries > 0:
        data = prompt(questions)
        res = post('api/auth/change_password', data, headers={'Authorization':token})
        if res.status_code == 204:
            #print_success('Password changed successfully.')
            on_success(res)
            success = True
            return Result(Status.SUCCESS, 'Password changed successfully.')
        else:
            on_failure(res)
            #print_error(res)
        tries -= 1
    return Result(Status.FAILURE, res)

def delete_account(on_success, on_failure, tries=200):
    #token = 'Token 2882ede988f3961c706dcc39320f4665160a2e67'
    token = user_token.get_token()
    logged_in = False
    while not logged_in and tries > 0:
        data = prompt(username + password)
        res = post('api/auth/delete', data, headers={'Authorization':token})
        if res.status_code == 200:
            #print_success("Account deleted successfully.")
            on_success(res)
            logged_in = True
            return Result(Status.SUCCESS, "Account deleted successfully.")
        else:
            #print_error(res)
            on_failure(res)
        tries -= 1
    return Result(Status.FAILURE, res)
