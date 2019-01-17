import os
from flask import Flask, render_template


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

    from . import account, inventarios, users
    app.register_blueprint(account.bp)
    app.register_blueprint(inventarios.bp)
    app.register_blueprint(users.bp)

    return app


def authorize(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not session.get('user_id'):
            return redirect(url_for('controllers.login'))
        return view(**kwargs)

    return wrapped_view
