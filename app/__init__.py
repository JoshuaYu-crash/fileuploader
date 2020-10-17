import click
from flask import Flask
from app.extension import *
from app.user import user
from app.model import *


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('setting.py')

    register_extensions(app)
    register_blueprint(app)
    register_command(app)

    return app


def register_extensions(app):
    db.init_app(app)


def register_blueprint(app):
    app.register_blueprint(user, url_prefix='/user')


def register_command(app):
    @app.cli.command()
    def initdb():
        db.drop_all()
        db.create_all()
        r.flushall()
        click.echo('create success')
