from __future__ import print_function, unicode_literals
import sys
import argparse
import logging
import colorama
from colorama import Fore, Style, AnsiToWin32
from PyInquirer import prompt, style_from_dict, Token, Validator, ValidationError

from .request_utils import post
from .account_manager import register, login, logout, change_password, delete_account

colorama.init(wrap=False)
stream = AnsiToWin32(sys.stderr).stream

def main():

    specified_register = lambda : register(on_success=lambda res : print_success('Account created!'), on_failure=print_error)
    specified_login = lambda : login(on_success=lambda res : print_success("You are logged in, welcome!"), on_failure=print_error)
    specified_change_password = lambda : change_password(on_success=lambda res : print_success('Password changed successfully.'), on_failure=print_error)
    specified_logout = lambda : logout(on_success=lambda res : print_success("You are logged out, see you!"), on_failure=print_error)
    specified_delete_account = lambda : delete_account(on_success=lambda res : print_success("Account deleted successfully."), on_failure=print_error)
    parser = argparse.ArgumentParser(prog='senpy')
    subparsers = parser.add_subparsers()

    subparsers.add_parser('register').set_defaults(func=specified_register)
    subparsers.add_parser('login').set_defaults(func=specified_login)
    subparsers.add_parser('logout').set_defaults(func=specified_logout)
    subparsers.add_parser('change_password').set_defaults(func=specified_change_password)
    subparsers.add_parser('delete_account').set_defaults(func=specified_delete_account)

    args = vars(parser.parse_args())

    if 'func' in args:
        args.pop('func')()
    else:
        parser.print_usage()
        return
   
def print_error(res):
    """

    prints error message 

    parameters :
    res : result of the query
    """
    def print_message(error):
        print(Fore.RED + "Senpy - " + error.lower() + Style.RESET_ALL, file=stream)

    if type(res) == str:
        print_message(res)
        return

    if 'python_error' in res:
        print_message(res['message'])
        return

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
    elif type(errors) == str:
        print_message(data)

def print_success(message):
    """

    prints succes of a query

    parameters :
    message : message to print
    """
    print(Fore.GREEN + message + Style.RESET_ALL)