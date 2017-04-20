Badger McBadgery
================

## Installation
### Virtual Environment/Python
1. Use Python 3 or go home and die in a fire.
2. Execute the following on the commandline where you've clone this project (inside the project's root folder):
    a. `python3 -m venv venv` 
        * The `-m venv` is the Python 3.5+ way of telling the Python binary to create a virtualenv.
        * The equivalent for Python 3.4 is `-m virtualenv`
3. Update the virtualenv's Pip to last version:
    `venv/bin/pip install -U pip`
4. Install Pypi requirements:
    `venv/bin/pip install -r ./requirements.txt`
5. Install Flake8 pre-commit hook:
    `venv/bin/flake8 --install-hook git` and `git config --bool flake8.strict true`
    a. This check will hinder you from committing files in Git if they do not pass the flake8 tests!
        However, it would be cruel to enforce this on all and every circumstance, so these tests can be ignored in git if
        append `--skip-verify` to your `git commit` command!
6. Your virtualenv is now ready to be activated (noob fashion), and it's executables are ready for utilization in the
    `venv/bin` (or `venv\Scripts` on Windblows) folder! (Pro fashion).

Example: `venv/bin/python <python script> <cmdline args>`(!)

# Linting
New with this commit is that [Flake8](https://pypi.python.org/pypi/flake8) is also an installed Pypi requirement.
Check step `5` above for for instructions!
   
