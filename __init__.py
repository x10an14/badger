#!flask/bin/python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask("badger")
app.config.from_object('config')
db = SQLAlchemy(app)


if __name__ == "__main__":
    app.run()