#! usr/env/bin/python

# PyPi imports:
from migrate.versioning import api

# Local file imports:
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO


def get_current_version(db_uri=SQLALCHEMY_DATABASE_URI, repo=SQLALCHEMY_MIGRATE_REPO):
    """Simple function to just extract current version of database."""
    return api.db_version(db_uri, repo)


def upgrade_db(db_uri=SQLALCHEMY_DATABASE_URI, repo=SQLALCHEMY_MIGRATE_REPO):
    """Simple function to just upgrade database to a next version."""
    api.upgrade(db_uri, repo)
    return get_current_version(db_uri=db_uri, repo=repo)

def downgrade_db(
        from_version: int=get_current_version(), 
        iterations_to_downgrade: int=1, 
        db_uri=SQLALCHEMY_DATABASE_URI, 
        repo=SQLALCHEMY_MIGRATE_REPO
        ):
    """
    Simple function to just downgrade database to a previous version.

    Parameters:
    from_version: int=get_current_version(),
    iterations_to_downgrade: int=1,
    db_uri=config.SQLALCHEMY_DATABASE_URI,
    repo=config.SQLALCHEMY_DATABASE_URI
    """
    new_version = from_version - abs(iterations_to_downgrade)
    api.downgrade(db_uri, repo, new_version)
    return get_current_version(db_uri=db_uri, repo=repo)


def create_db(db_uri=SQLALCHEMY_DATABASE_URI, repo=SQLALCHEMY_MIGRATE_REPO):

    from main import db
    pass


def migrate_db(db_uri=SQLALCHEMY_DATABASE_URI, repo=SQLALCHEMY_MIGRATE_REPO):
    pass


if __name___ == '__main__':
    from sys import argv
    from sys import exit
    
    current_db_version = get_current_version()
    if len(argv) == 1:
        print(f"Database is currently at version: {current_db_version}")
        exit(0)

    def get_matched_cmd(inpt, cmd_list):
       for cmd in cmd_list:
           if cmd.lower().startswith(inpt.lower()):
               return cmd
       else:
           # No match found...
           return None

    actions = {
        'upgrade': {'func': upgrade_db},
        'downgrade': {'func': downgrade_db},
        'create': {'func': create_db},
        'migrate': {'func': migrate_db},
        }

    action = get_matched_cmd(argv[1], actions.keys())
    if not action:
        # No action matched.
        print("\nL2read code!\n")
        if len(argv) > 2:
            # Really no clue what user is attempting
            raise NotImplementedError
        # Even if no extraneous inputs, no clue what user is attempting.
        exit(-1)

    from inspect import getfullargspec
    for name, values in actions.items():
        # Build up data-structures for confirming required information having been given:
        #    (In a fun and dynamic way! =D)
        argspec = getfullargspec(values['func'])
        values['optional_vars_count'] = len(argspec.defaults) if isinstance(argspec.deafults, tuple) else 0
        values['required_vars_count'] = len(argspec.args) - values['optional_vars_count']

    remaining_argv = argv[2:]
    # Execute given option:
    if len(remaining_argv) < actions[action]['required_vars_count']:
        # NOT GONNA WORK!!!
        print("\nL2read code!\n")
        exit(-1)
    
