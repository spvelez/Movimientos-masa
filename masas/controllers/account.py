from flask import (
     Blueprint, flash, render_template, redirect, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from masas import authorize
from masas.forms import ChangePasswordForm
from masas.models.user import User
from masas.database import session as db_session

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
            session['user_role'] = user.role
            return redirect(url_for('index'))

    return render_template('login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@bp.route('/changepassword', methods=['GET', 'POST'])
@authorize()
def change_password():
    form = ChangePasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter(User.id == session['user_id']).first()

        if not check_password_hash(user.password, form.password.data):
            flash('La contraseña actual es incorrecta')
        else:
            new_password = form.new_password.data
            user.password = generate_password_hash(new_password)
            db_session.commit()

            return redirect(url_for('index'))

    return render_template('changepassword.html', form=form)
