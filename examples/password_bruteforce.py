"""

SenPy can, of course, be useful in applications that aren't Data Science related. 
In fact it can be used for any long computation you encounter in python, especially
if it is difficult to estimate the time required to perform the task. 
Here's an example in cryptography with brute force of a password using hashes,
which is a traditional cyber security class exercise.
"""


import requests
import hashlib
from urllib.request import urlopen

# importing senpy
from senpy import notify_me, ntm



# fetch the common passwords online
COMMON_PASSWORDS = str(requests.get("https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/probable-v2-top12000.txt").content).split('\\')

SEEKED_HASH = '5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8'


def hash(password):
    result = hashlib.sha1(password.encode())
    return result.hexdigest()

def bruteforce(common_password_list, actual_password_hash):

    # ========================================= #
    with ntm(common_password_list) as common_passwords:
    # with ntm, SenPy let's you keep track of the amount of hashed studied
    # ========================================== #
        
        for guess_password in common_passwords:
            if hash(guess_password) == actual_password_hash:
                return guess_password


if __name__ == '__main__':
    

    password = bruteforce(COMMON_PASSWORDS, SEEKED_HASH)

    # with notify_me, SenPy let's you know when the script is done and
    # if it returned a successful result
    notify_me(f"password found : {password}" if password is not None else "None of the common passwords matched")
