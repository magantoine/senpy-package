import argparse
from .account_manager import register, login, logout, change_password, delete_account
from .request_utils import print_success, print_error

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
