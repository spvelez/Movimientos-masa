import os
import functools
from flask import Flask, flash, redirect, render_template, session, url_for


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.update(test_config)

    if not os.path.isdir(app.instance_path):
        os.makedirs(app.instance_path)

    with app.app_context():
        from . import database
        database.init_app(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    from .controllers import account, api, movimientos, users
    app.register_blueprint(account.bp)
    app.register_blueprint(api.bp)
    app.register_blueprint(movimientos.bp)
    app.register_blueprint(users.bp)

    return app


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
