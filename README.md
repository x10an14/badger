Badger McBadgery
================

## Installation
### Virtual Environment/Python
1. Use Python 3 or go home and die in a fire.
2. Execute the following on the commandline where you've clone this project (inside the project's root folder): ```python3 -m venv venv```
    1. The `-m venv` is the Python 3.5+ way of telling the Python binary to create a virtualenv.
    2. The equivalent for Python 3.4 is `-m virtualenv`
3. Update the virtualenv's Pip to last version:
    ```venv/bin/pip install -U pip```
4. Install Pypi requirements:
    ```venv/bin/pip install -r ./requirements.txt```
5. Install Flake8 pre-commit hook:
    ```venv/bin/flake8 --install-hook git``` and ```git config --bool flake8.strict true```
6. Your virtualenv is now ready to be activated (noob fashion), and it's executables are ready for utilization in the
    `venv/bin` (or `venv\Scripts` on Windblows) folder! (Pro fashion).

## Execution

Example: `venv/bin/python <python script> <cmdline args>`

### General program
From the commandline you've got a newb alternative:
```
venv/bin/activate
python ./main.py
```
or the pro alternative:
```
venv/bin/python ./main.py
```

### Database stuffs
* Create database:
```
venv/bin/python db_create.py
```
* Upgrade database:
```
venv/bin/python db_create.py
```
* Downgrade database:
```
venv/bin/python db_create.py
```
* Migrate database:
```
venv/bin/python db_create.py
```

# Linting
[Flake8](https://pypi.python.org/pypi/flake8) is an installed Pypi requirements.txt requirement.
Check step `5` above for for install instructions!
   
