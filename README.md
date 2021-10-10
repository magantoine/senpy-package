# Senpy package

## Usage
In the command line you can register an account and handle all the authentication measures:
```bash
senpy register
>>> ? Username: your_username
>>> ? Password: *********
>>> ? Confirmation: *********
```

The existing commands are:
```bash
senpy {register|login|logout|change_password|delete_account}
```

Now in any python screen you like you can do 

```python
import senpy
``` 

and indeed get the package's function

## To contribute

### Architecture 

The directory ```senpy_package``` is, for now built as follows :
```
├───senpy # Folder containing the source code
    ├───manage.py # Django management script
    ├───senpy # Project setup
    └───
├───tests
    ├───manage.py # Django management script
    ├───senpy # Project setup
    └───
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











