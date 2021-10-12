<img alt="SenPy" src="./assets/banner.png"> 

## What is it?

*Notify Me SenPy* is a tool that let's you track your Python scripts' execution and receive a notification whenever the execution reaches certain points.

It is composed of a PyPi package and a mobile app. The package is used in your Python script to specify which job you want to track and at which points you want to receive notifications. The application is where you can check on your job progress and see the notification history.

<p float="center">
<img src="./assets/jobs.png" alt="job screen" />
</p>

## Usage

You can send notifications from a script to your app using `notify_me`
```python
from senpy import notify_me

notify_me("Great job!")
```

You can track your jobs using the `ntm` python `with statement`:

```python
from senpy import ntm
from time import sleep 

with ntm(range(10)) as iterator:
    for i, item in enumerate(iterator):
        sleep(5)
``` 

## Installation
### 1. Package
First install the *Notify Me SenPy* PyPi package
```bash
pip install notify-me-senpy
```

Create an account from the command line
```bash
senpy register
>>> ? Username: your_username
>>> ? Password: *********
>>> ? Password confirmation: *********
```

The existing commands are
```bash
senpy {register|login|logout|change_password|delete_account}
```
You are done with the package setup! 🎉

### 2. App

Download the *Notify Me SenPy* app from the store.

Once the app installed, open the app and wait until the configuration is done. You should receive a notification confirming that the configuration has been successfully completed. Otherwise, check your connection, try again or try re-installing the app.

Once done, you simply have to log into your account in the app to complete the installation.
<p float="center">
<img src="./assets/login.png" alt="login screen"/>
</p>


## To contribute

### Architecture 

The directory ```senpy_package``` is, at this time, built as follows :
```bash
├───senpy # Folder containing the source code
    ├───account_manager.py # authentication system
    ├───cli.py # cli utility functions
    ├───jobs.py # ntm with statement source code
    ├───notifications.py # notify_me source code
    ├───request_utils.py # HTTP methods
    └───user_token.py # Auth-token-related functions
├───tests # Unittests for each function
    ├───notify_me.py 
    └───ntm.py
└───setup.py # Package configuration file
```


### Development

To get started, you can create a virtual environnement and install the packages listed in `requirements.txt`:
```
git clone https://github.com/magantoine/senpy-package
pip install virtualenv
virtualenv venv
source venv/bin/activate
cd senpy-package
pip install -r requirements.txt
```

Run the following command from the top folder:
```
pip install --editable .
```
You only need to run this command once. What it does is that it installs a package, called `senpy`, whose implementation is in the current folder (and not in the usual `site-packages`), so every subsequent code modifications while be taken into account.
You can directly go to the Usage section.