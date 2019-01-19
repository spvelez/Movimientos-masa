from flask import (
     Blueprint, flash, render_template, redirect, request, session, url_for
)
from werkzeug.security import check_password_hash
from .models.user import User

bp = Blueprint('account', __name__, template_folder='templates')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        user = User.query.filter(User.login == login).first()

        if user is None or not check_password_hash(user.password, password):
            flash('Usuario o contraseña incorrectos')
        else:
            session.clear()
            session['user_id'] = user.id
            session['user_login'] = user.login
            return redirect(url_for('index'))

    return render_template('login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
