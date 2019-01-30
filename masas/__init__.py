import os
import functools
from flask import Flask, flash, redirect, render_template, session, url_for


class AppBuilder:
    def __init__(self):
        self.app = Flask(__name__, instance_relative_config=True)

    def load_config(self, test_config=None):
        if test_config is None:
            self.app.config.from_pyfile('config.py', silent=True)
        else:
            self.app.config.update(test_config)

        if not os.path.isdir(self.app.instance_path):
            os.makedirs(self.app.instance_path)

    def init_db(self):
        with self.app.app_context():
            from . import database

            self.app.teardown_appcontext(database.close_db)
            self.app.cli.add_command(database.init_db_command)

    def register_routes(self):
        @self.app.route('/')
        def index():
            return render_template('index.html')

        from .controllers import account, api, movimientos, users
        self.app.register_blueprint(account.bp)
        self.app.register_blueprint(api.bp)
        self.app.register_blueprint(movimientos.bp)
        self.app.register_blueprint(users.bp)


def create_app(test_config=None):
    builder = AppBuilder()

    builder.load_config(test_config)
    builder.init_db()
    builder.register_routes()

    return builder.app


def authorize(role=None):
    def wrapper(view):
        @functools.wraps(view)
        def wrapped_view(*args, **kwargs):
            if not session.get('user_id'):
                return redirect(url_for('account.login'))
            elif role and session.get('user_role') != role.value[0]:
                flash('No tienes permiso para esta sección')
                return redirect(url_for('account.login'))
            return view(*args, **kwargs)

        return wrapped_view

    return wrapper
