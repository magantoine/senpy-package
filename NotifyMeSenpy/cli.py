from __future__ import print_function, unicode_literals
from PyInquirer import prompt, style_from_dict, Token, Validator, ValidationError
from .request_utils import post
from colorama import Fore, Style
import argparse

# style = style_from_dict({
#     Token.Separator: '#cc5454',
#     Token.QuestionMark: '#673ab7 bold',
#     Token.Selected: '#cc5454',  # default
#     Token.Pointer: '#673ab7 bold',
#     Token.Instruction: '',  # default
#     # Token.Answer: '#f44336 bold',
#     Token.Question: '',
# })

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

def register():
    questions = username + password + [
        {
            'type': 'password',
            'message': 'Password confirmation',
            'name': 'password_confirmation',
        }]
    registered = False
    while not registered:
        data = prompt(questions)
        res = post('api/auth/register', data)
        if res.status_code == 201:
            token = res.json()['auth_token']
            user_id = res.json()['id']
            print(user_id)
            print_success('Account created!')
            registered = True
        else:
            print_error(res)

def login():
    logged_in = False
    while not logged_in:
        data = prompt(username + password)
        res = post('api/auth/login', data)
        if res.status_code == 200:
            print_success("You are logged in, welcome!")
            token = res.json()['auth_token']
            logged_in = True
        else:
            print_error(res)

def logout():
    token = '2882ede988f3961c706dcc39320f4665160a2e67'
    res = post('api/auth/logout', headers={'Authentication': token})
    print_success("You are logged out, see you!")
    
def change_password():
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
    token = 'Token 2882ede988f3961c706dcc39320f4665160a2e67'
    while not success:
        data = prompt(questions)
        res = post('api/auth/change_password', data, headers={'Authorization':token})
        if res.status_code == 204:
            print_success('Password changed successfully.')
            success = True
        else:
            print_error(res)

def delete_account():
    token = 'Token 2882ede988f3961c706dcc39320f4665160a2e67'
    logged_in = False
    while not logged_in:
        data = prompt(username + password)
        res = post('api/auth/delete', data, headers={'Authorization':token})
        if res.status_code == 200:
            print_success("Account deleted successfully.")
            logged_in = True
        else:
            print_error(res)

def main():
    parser = argparse.ArgumentParser(prog='senpy')
    subparsers = parser.add_subparsers()

    subparsers.add_parser('register').set_defaults(func=register)
    subparsers.add_parser('login').set_defaults(func=login)
    subparsers.add_parser('logout').set_defaults(func=logout)
    subparsers.add_parser('change_password').set_defaults(func=change_password)
    subparsers.add_parser('delete_account').set_defaults(func=delete_account)

    args = vars(parser.parse_args())

    if 'func' in args:
        args.pop('func')()
    else:
        parser.print_usage()
        return
   
def print_error(res):
    def parse_message(error):
        return Fore.RED + error.lower().capitalize() + Style.RESET_ALL
    data = res.json()
    if type(data) == list:
        for error in data:
            print(parse_message(error))
    elif type(data) == dict:
        for key, errors in data.items():
            for error in errors:
                print(parse_message(error))
    else:
        print(parse_message(data))

def print_success(message):
    print(Fore.GREEN + message + Style.RESET_ALL)