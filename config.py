from os import path as op
basedir = op.dirname(op.abspath(op.realpath(__file__)))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + op.join(basedir, "app.db")
SQLALCHEMY_MIGRATE_REPO = op.join(basedir, "db_repository")
